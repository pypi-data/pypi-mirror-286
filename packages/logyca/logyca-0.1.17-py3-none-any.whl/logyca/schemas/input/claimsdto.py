from pydantic import BaseModel,Field

class ClaimsDTO(BaseModel):
    email:str=Field(default='',description="Email from user")
    expirationTimeUTCBogota:str=Field(default='',description="Expiration data from user token")
    name:str=Field(default='',description="User name")
    token:str=Field(default='',description="Bearer token")
