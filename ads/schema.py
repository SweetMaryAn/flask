from pydantic import BaseModel
from pydantic import ValidationError
from errors import HttpError

class CreateAd(BaseModel):

    username: str
    heading: str



def validate_create_ads(json_data):
    try:
        ad_schema = CreateAd(**json_data)
        return ad_schema.model_dump()
    except ValidationError as er:
       raise HttpError(status_code=400, message=er.errors())


