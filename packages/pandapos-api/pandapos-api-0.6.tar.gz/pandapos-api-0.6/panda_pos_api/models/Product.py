

from pydantic import BaseModel

class ProductPortion(BaseModel):

    name: str
    price: float
    multiplier: int


class ProductTag(BaseModel):
    name: str
    value: str
    

class Product(BaseModel):
    
    name: str
    groupCode: str
    barcode: str
    portions: list[ProductPortion]
    tags: list[ProductTag]