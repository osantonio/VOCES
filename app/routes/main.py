"""
Rutas principales de la aplicación.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.core import templates

router = APIRouter(tags=["General"])


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Endpoint raíz que renderiza la página de inicio.
    """
    return templates.TemplateResponse("index.html", {"request": request})
