from pydantic.v1 import BaseModel as PydanticBaseModel
from fastapi.responses import JSONResponse


class BaseModel(PydanticBaseModel):
    def e(self, prefix: str = "data: ", sep: str = "\n\n") -> str:
        return f"{prefix}{self.json()}{sep}"

    class Config:
        arbitrary_types_allowed = True


class BaseOutput(BaseModel):
    code: int = 200
    msg: str = "success"

    def r(self):
        return JSONResponse(self.dict(), status_code=self.code)

    class Config:
        extra = "allow"


class ErrorMessage(BaseOutput):
    code: int = 500
    msg: str = "failed"
