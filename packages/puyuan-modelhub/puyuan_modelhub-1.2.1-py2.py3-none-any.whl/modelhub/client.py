from modelhub.utils import BaseModel, retrieve_top_k
import json
import os
import numpy as np
from functools import partial
from io import TextIOWrapper
from typing import Any, Dict, Generator, List, Literal, Optional, Union, AsyncGenerator

import httpx
import retrying
from httpx import Response

from modelhub.types import (
    BaseMessage,
    ChatParameters,
    CrossEncoderOutput,
    CrossEncoderParams,
    EmbeddingOutput,
    ModelInfo,
    ModelInfoOutput,
    NTokensOutput,
    TextGenerationOutput,
    TextGenerationStreamOutput,
    Transcription,
)
from modelhub.types.retrieve import RerankOutput, RetrieveOutput
from modelhub.types import errors as err
from modelhub.types.errors import STATUS_CODE as s


RETRY_EXCEPTIONS = (
    err.RateLimitError,
    err.APIConnectionError,
    err.APITimeoutError,
)


def retry_on_exception(e):
    return isinstance(e, RETRY_EXCEPTIONS)


class ModelhubClient(BaseModel):
    """
    ModelhubClient: A Python client for the Modelhub API
    """

    user_name: str = os.getenv("MODELHUB_USER_NAME", "")
    """user name for authentication"""
    user_password: str = os.getenv("MODELHUB_USER_PASSWORD", "")
    """user password for authentication"""
    host: str = os.getenv("MODELHUB_HOST", "")
    model: str = ""
    max_retries: int = 3
    wait_fixed: int = 1000
    timeout: Optional[Union[httpx.Timeout, float]] = 600
    """host URL of the Modelhub API"""
    """list of supported models"""
    headers: Dict[str, Any] = {}

    class Config:
        arbitrary_types_allowed = True
        extra = "forbid"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.headers["Authorization"] = f"{self.user_name}:{self.user_password}"
        self.host = self.host.rstrip("/")

    @property
    def supported_models(self) -> Dict[str, ModelInfo]:
        return self._get_supported_models()

    def _check_status(self, response: Response):
        if response.status_code == 200:
            return

        try:
            err_msg = json.loads(response.text)["msg"]
        except Exception:
            err_msg = response.text
        if response.status_code == s.UNAUTHORIZED:
            raise err.AuthenticationError(msg=err_msg)
        elif response.status_code == s.MODEL_NOT_FOUND:
            raise err.ModelNotFoundError(msg=err_msg)
        elif response.status_code == s.MODEL_NOT_STARTED:
            raise err.ModelNotStartedError(msg=err_msg)
        elif response.status_code == s.BAD_PARAMS:
            raise err.BadParamsError(msg=err_msg)
        elif response.status_code == s.API_RATE_LIMIT:
            raise err.RateLimitError(msg=err_msg)
        elif response.status_code == s.BILL_LIMIT:
            raise err.BillLimitError(msg=err_msg)
        elif response.status_code == s.INTERNAL_ERROR:
            raise err.ModelGenerateError(msg=err_msg)
        elif response.status_code == s.API_TIMEOUT:
            raise err.APITimeoutError(msg=err_msg)
        elif response.status_code == s.API_CONNECTION_ERROR:
            raise err.APIConnectionError(msg=err_msg)
        else:
            raise err.ModelhubException(code=response.status_code, msg=err_msg)

    @retrying.retry(
        wait_fixed=wait_fixed,
        stop_max_attempt_number=max_retries,
        retry_on_exception=retry_on_exception,
    )
    def _post(
        self,
        url: str,
        method: Literal["get", "post"] = "post",
        **kwargs,
    ) -> Response:
        """Make a GET request"""
        r = getattr(httpx, method)(
            url=url, timeout=self.timeout, headers=self.headers, **kwargs
        )
        self._check_status(r)
        return r

    @retrying.retry(
        wait_fixed=wait_fixed,
        stop_max_attempt_number=max_retries,
        retry_on_exception=retry_on_exception,
    )
    async def _apost(self, url: str, **kwargs) -> Response:
        async with httpx.AsyncClient() as client:
            r = await client.post(
                url, headers=self.headers, timeout=self.timeout, **kwargs
            )
            self._check_status(r)
            return r

    def _get_supported_models(self) -> ModelInfoOutput:
        """Get a list of supported models from the Modelhub API"""
        response = self._post(
            self.host + "/models",
            method="get",
        )
        return ModelInfoOutput(**response.json()).models

    def n_tokens(
        self,
        prompt: str | List[Union[BaseMessage, Dict[str, Any]]],
        model: str = "",
        params={},
    ) -> NTokensOutput:
        """
        Get the number of tokens in a prompt
        params:
            prompt: the prompt
            model: the model name
        """
        model = model or self.model
        response = self._post(
            self.host + "/tokens",
            json={
                "prompt": prompt,
                "model": model,
                "params": params,
            },
        )
        return NTokensOutput(**response.json())

    def _prepare_chat_args(
        self,
        prompt: str
        | List[Union[BaseMessage, Dict[str, Any]]]
        | Union[BaseMessage, Dict[str, Any]],
        model: str = "",
        history: List[Union[BaseMessage, Dict[str, Any]]] = [],
        return_type: Literal["text", "json", "regex"] = "text",
        return_schema: Union[Dict[str, Any], str, None] = None,
        parameters: ChatParameters = {},
        *,
        stream: bool = False,
        **kwargs,
    ):
        model = model or self.model
        if isinstance(prompt, list) and history:
            raise err.BadParamsError(msg="prompt and history cannot both be lists")
        if isinstance(prompt, (BaseMessage, dict)):
            prompt = [prompt]
        if isinstance(prompt, list):
            prompt = [m.dict() if isinstance(m, BaseMessage) else m for m in prompt]
        parameters["history"] = [
            m.dict() if isinstance(m, BaseMessage) else m for m in history
        ]
        parameters["return_type"] = return_type
        parameters["schema"] = return_schema
        return {
            "prompt": prompt,
            "model": model,
            "parameters": {**parameters, **kwargs},
            "stream": stream,
        }

    def chat(
        self,
        prompt: str | List[Union[BaseMessage, Dict[str, Any]]],
        model: str = "",
        history: List[Union[BaseMessage, Dict[str, Any]]] = [],
        return_type: Literal["text", "json", "regex"] = "text",
        return_schema: Union[Dict[str, Any], str, None] = None,
        parameters: ChatParameters = {},
        **kwargs,
    ) -> TextGenerationOutput:
        response = self._post(
            self.host + "/chat",
            json=self._prepare_chat_args(
                prompt=prompt,
                model=model,
                history=history,
                return_type=return_type,
                return_schema=return_schema,
                parameters=parameters,
                **kwargs,
            ),
        )
        return TextGenerationOutput.parse_raw(response.text)

    def batch_chat(
        self,
        batch_prompts: List[str],
        model: str = "",
        batch_parameters: List[ChatParameters] = [],
    ):
        model = model or self.model
        response = self._post(
            self.host + "/batch_chat",
            json={
                "batch_prompts": batch_prompts,
                "model": model,
                "batch_parameters": batch_parameters,
            },
        )
        outputs = response.json()
        return [TextGenerationOutput.parse_obj(o) for o in outputs]

    async def abatch_chat(
        self,
        batch_prompts: List[str],
        model: str = "",
        batch_parameters: List[ChatParameters] = [],
    ):
        model = model or self.model
        response = await self._apost(
            self.host + "/batch_chat",
            json={
                "batch_prompts": batch_prompts,
                "model": model,
                "batch_parameters": batch_parameters,
            },
        )
        outputs = response.json()
        return [TextGenerationOutput.parse_obj(o) for o in outputs]

    async def achat(
        self,
        prompt: str | List[Union[BaseMessage, Dict[str, Any]]],
        model: str = "",
        history: List[BaseMessage] = [],
        return_type: Literal["text", "json", "regex"] = "text",
        return_schema: Union[Dict[str, Any], str, None] = None,
        parameters: ChatParameters = {},
        **kwargs,
    ) -> TextGenerationOutput:
        response = await self._apost(
            self.host + "/chat",
            json=self._prepare_chat_args(
                prompt=prompt,
                model=model,
                history=history,
                return_type=return_type,
                return_schema=return_schema,
                parameters=parameters,
                **kwargs,
            ),
        )
        return TextGenerationOutput.parse_raw(response.text)

    @retrying.retry(
        wait_fixed=wait_fixed,
        stop_max_attempt_number=max_retries,
        retry_on_exception=retry_on_exception,
    )
    def stream_chat(
        self,
        prompt: str | List[Union[BaseMessage, Dict[str, Any]]],
        model: str = "",
        history: List[BaseMessage] = [],
        parameters: Dict[str, Any] = {},
        **kwargs,
    ) -> Generator[TextGenerationStreamOutput, None, None]:
        with httpx.Client() as client:
            with client.stream(
                "post",
                url=self.host + "/chat",
                headers=self.headers,
                timeout=self.timeout,
                json=self._prepare_chat_args(
                    prompt=prompt,
                    model=model,
                    history=history,
                    parameters=parameters,
                    stream=True,
                    **kwargs,
                ),
            ) as r:
                for line in r.iter_lines():
                    if line.startswith("data:"):
                        self._check_status(r)
                        yield TextGenerationStreamOutput.parse_raw(line[5:])

    @retrying.retry(
        wait_fixed=wait_fixed,
        stop_max_attempt_number=max_retries,
        retry_on_exception=retry_on_exception,
    )
    async def astream_chat(
        self,
        prompt: str | List[Union[BaseMessage, Dict[str, Any]]],
        model: str = "",
        history: List[BaseMessage] = [],
        parameters: Dict[str, Any] = {},
        **kwargs,
    ) -> AsyncGenerator[TextGenerationStreamOutput, None]:
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "post",
                url=self.host + "/chat",
                headers=self.headers,
                timeout=self.timeout,
                json=self._prepare_chat_args(
                    prompt=prompt,
                    model=model,
                    history=history,
                    parameters=parameters,
                    stream=True,
                    **kwargs,
                ),
            ) as r:
                async for line in r.aiter_lines():
                    if line.startswith("data:"):
                        self._check_status(r)
                        yield TextGenerationStreamOutput.parse_raw(line[5:])

    def retrieve(
        self,
        querys: list[str] | str,
        passages: list[str],
        model: str | None = None,
        embedding_params: Dict[str, Any] = {},
        top_k: int = 5,
        threshold: float = 0.0,
    ):
        model = model or self.model
        if isinstance(querys, str):
            querys = [querys]
        embedding = partial(
            self.get_embeddings, model=model, parameters=embedding_params
        )
        query_embeddings = np.array(embedding(querys).embeddings)
        passage_embeddings = np.array(embedding(passages).embeddings)
        return RetrieveOutput(
            **retrieve_top_k(
                passages,
                query_embeddings,
                passage_embeddings,
                top_k,
                threshold,
            )
        )

    async def aretrieve(
        self,
        querys: list[str] | str,
        passages: list[str],
        model: str | None = None,
        embedding_params: Dict[str, Any] = {},
        top_k: int = 5,
        threshold: float = 0.0,
    ):
        model = model or self.model
        if isinstance(querys, str):
            querys = [querys]
        embedding = partial(
            self.aget_embeddings, model=model, parameters=embedding_params
        )
        query_embeddings = np.array((await embedding(querys)).embeddings)
        passage_embeddings = np.array((await embedding(passages)).embeddings)
        return RetrieveOutput(
            **retrieve_top_k(
                passages,
                query_embeddings,
                passage_embeddings,
                top_k,
                threshold,
            )
        )

    def rerank(
        self,
        query: str,
        docs: list[str],
        model: str | None = None,
        parameters: Dict[str, Any] = {},
        top_k: int = 5,
        threshold: float = 0.0,
    ):
        pairs = [[query, doc] for doc in docs]
        scores = np.array(
            self.cross_embedding(pairs, model=model, parameters=parameters).scores
        )
        idxs = np.argsort(scores)[::-1][:top_k]
        idxs = idxs[scores[idxs] > threshold]
        return RerankOutput(
            passages=[docs[i] for i in idxs],
            idxs=idxs.tolist(),
            scores=scores[idxs].tolist(),
        )

    async def arerank(
        self,
        query: str,
        docs: list[str],
        model: str | None = None,
        parameters: Dict[str, Any] = {},
        top_k: int = 5,
        threshold: float = 0.0,
    ):
        pairs = [[query, doc] for doc in docs]
        scores = np.array(
            (
                await self.across_embedding(pairs, model=model, parameters=parameters)
            ).scores
        )
        idxs = np.argsort(scores)[::-1][:top_k]
        idxs = idxs[scores[idxs] > threshold]
        return RerankOutput(
            passages=[docs[i] for i in idxs],
            idxs=idxs.tolist(),
            scores=scores[idxs].tolist(),
        )

    def get_embeddings(
        self, prompt: str, model: str = "", parameters: Dict[str, Any] = {}
    ) -> EmbeddingOutput:
        model = model or self.model
        response = self._post(
            self.host + "/embedding",
            json={
                "prompt": prompt,
                "model": model,
                "parameters": parameters,
            },
        )
        return EmbeddingOutput(**response.json())

    async def aget_embeddings(
        self, prompt: str, model: str = "", parameters: Dict[str, Any] = {}
    ) -> EmbeddingOutput:
        model = model or self.model
        response = await self._apost(
            self.host + "/embedding",
            json={
                "prompt": prompt,
                "model": model,
                "parameters": parameters,
            },
        )
        return EmbeddingOutput(**response.json())

    def cross_embedding(
        self,
        sentences: List[List[str]],
        model: str = "",
        parameters: CrossEncoderParams = {},
    ) -> CrossEncoderOutput:
        model = model or self.model
        res = self._post(
            self.host + "/cross_embedding",
            json={
                "sentences": sentences,
                "model": model,
                "parameters": parameters,
            },
        )
        return CrossEncoderOutput(**res.json())

    async def across_embedding(
        self,
        sentences: List[List[str]],
        model: str = "",
        parameters: CrossEncoderParams = {},
    ) -> CrossEncoderOutput:
        model = model or self.model
        res = await self._apost(
            self.host + "/cross_embedding",
            json={
                "sentences": sentences,
                "model": model,
                "parameters": parameters,
            },
        )
        return CrossEncoderOutput(**res.json())

    def transcribe(
        self,
        file: Union[str, TextIOWrapper],
        model: str = "",
        language: str = "",
        temperature: float = 0.0,
    ) -> Transcription:
        model = model or self.model
        if isinstance(file, str):
            file = open(file, "rb")

        r = self._post(
            url=self.host + "/audio/transcriptions",
            files={"file": file},
            data={
                "model": model,
                "language": language,
                "temperature": temperature,
            },
        )
        self._check_status(r)
        return Transcription(**r.json())

    async def atranscribe(
        self,
        file: Union[str, TextIOWrapper],
        model: str = "",
        language: str = "",
        temperature: float = 0.0,
    ) -> Transcription:
        model = model or self.model
        if isinstance(file, str):
            file = open(file, "rb")

        r = await self._apost(
            url=self.host + "/audio/transcriptions",
            files={"file": file},
            data={
                "model": model,
                "language": language,
                "temperature": temperature,
            },
        )
        self._check_status(r)
        return Transcription(**r.json())
