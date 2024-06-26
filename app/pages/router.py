from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.hotels.router import find_hotel_by_location

router = APIRouter(
    prefix='/pages',
    tags=['Фронтэнд']
)

templates = Jinja2Templates(directory="app/templates")


@router.get('/hotels')
async def get_hotels_page(
    request: Request,
    hotels=Depends(find_hotel_by_location)
):
    return templates.TemplateResponse(
        name='hotels.html', 
        context={"request": request, "hotels": hotels}
        )
