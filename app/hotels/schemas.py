from typing import List

from pydantic import BaseModel, ConfigDict


class SHotelInfo(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str 
    location: str 
    services: List[str] 
    rooms_quantity: int 
    image_id: int

    

class SHotelsList(SHotelInfo):

    model_config = ConfigDict(from_attributes=True)
    
    rooms_left: int
