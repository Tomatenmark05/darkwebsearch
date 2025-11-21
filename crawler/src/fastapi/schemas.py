from pydantic import BaseModel, field_validator
from typing import List, Union

# To convert a single string address into a list of addresses (e.g {"addresses": "address1"} -> {"addresses": ["address1"]})
class CrawlRequest(BaseModel):
    addresses: Union[str, List[str]]

    @field_validator("addresses") #pre=True to modify input before validation
    @classmethod
    def ensure_list(cls, value):
        if isinstance(value, str):
            return [value]
        return value
