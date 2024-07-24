




from typing import Optional
from pydantic import BaseModel


class OrderState(BaseModel):
    stateName: Optional[str]
    state: Optional[str]
    stateValue: Optional[str]

class OrderTag(BaseModel):
    tagName: Optional[str]
    tag: Optional[str]
    price: float
    rate: float
    quantity: float
    note: Optional[str]
    

class Order(BaseModel):
    id: int
    uid: str
    name: Optional[str]
    menuItemName: Optional[str]
    quantity: float
    enforceQuantity: bool
    price: float
    portion: Optional[str]
    calculatePrice: bool
    decreaseInventory: bool
    increaseInventory: bool
    states: Optional[list[OrderState]]
    tags: Optional[list[OrderTag]]


class TicketEntity(BaseModel):
    entityType: Optional[str]
    name: Optional[str]


class TicketState(BaseModel):
    stateName: Optional[str]
    state: Optional[str]
    stateValue: Optional[str]
    quantityExp: Optional[str]

class TicketTag(BaseModel):
    tagName: Optional[str]
    tag: Optional[str]

class TicketCalculation(BaseModel):
    name: Optional[str]
    amount: float

class Ticket(BaseModel):
    
    id: Optional[int]
    uid: Optional[str]
    type: Optional[str]
    date: Optional[str]
    department: Optional[str]
    terminal: Optional[str]
    user: Optional[str]
    number: Optional[str]
    note: Optional[str]
    orders: Optional[list[Order]]
    entities: Optional[list[TicketEntity]]
    tags: Optional[list[TicketTag]]
    calculations: Optional[list[TicketCalculation]]
