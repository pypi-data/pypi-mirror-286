from logyca.schemas.output.apifilterexceptiondto import ApiFilterExceptionDTO
from logyca.schemas.output.tokensdto import TokensDTO
from pydantic import BaseModel,Field
from typing import Any
from uuid import UUID, uuid4

class APIResultDTO(BaseModel):
        resultToken:TokensDTO=Field(default=TokensDTO(),description="Gets or sets object with result")
        resultObject:Any=Field(default=None,description="Gets or sets object with result")
        apiException:ApiFilterExceptionDTO=Field(description="Gets or sets error")
        resultMessage:str=Field(default='',description="Gets or sets result of negative or positive message")
        dataError:bool=Field(default=False,description="Gets or sets a value indicating whether gets or sets a value if it is data error")
        def __init__(self, **kwargs):
                kwargs['apiException'] = ApiFilterExceptionDTO()
                super().__init__(**kwargs)
        def to_dict(self):
                aPIResultDTO=self.__dict__.copy()
                aPIResultDTO["resultToken"]=aPIResultDTO["resultToken"].to_dict()
                aPIResultDTO["apiException"]=aPIResultDTO["apiException"].to_dict()
                return aPIResultDTO

class ValidationError(BaseModel):
        detailError: str = Field(default="")
        transactionId: str = Field(default="")
        def to_dict(self):
                return self.__dict__        

class APIResultDTOExternal(APIResultDTO):
        validationErrors: list[ValidationError] | None = Field(default=[])
        traceAbilityId: UUID  = Field(default=uuid4)
        def to_dict(self):
                aPIResultDTO=self.__dict__.copy()
                aPIResultDTO["resultToken"]=aPIResultDTO["resultToken"].to_dict()
                aPIResultDTO["apiException"]=aPIResultDTO["apiException"].to_dict()
                aPIResultDTO["traceAbilityId"]=str(aPIResultDTO["traceAbilityId"])
                aPIResultDTO["validationErrors"]=[validationError.to_dict() for validationError in aPIResultDTO["validationErrors"]]
                return aPIResultDTO
