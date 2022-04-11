from typing import Optional

from fastapi import APIRouter

from src.modules.parser.model import NyaaResponse, TorrentResponse
from src.modules.parser.parser import Nyaa

router = APIRouter(
    prefix="/api/v1/nyaa",
    tags=["Nyaa"]
)

nyaa = Nyaa()


@router.get(
    path="",
    response_model=NyaaResponse
)
async def nyaa_search(
        query: Optional[str] = "",
        category: Optional[int] = 0,
        subcategory: Optional[int] = 0,
        page: Optional[int] = 1,
        sort: Optional[str] = "id",
        order: Optional[str] = "desc",
        filter: Optional[int] = 0
):
    """
     Search on nyaa.si:

     - **query**: search keyword string (default: "")
     - **category**: category id (default: 0)
     - **subcategory**: subcategory id (default: 0)
     - **filter**: filter id (default: 0)
     - **page**: page number, supports pagination (default: 1)
     - **sort**: sort id (default: "id")
     - **order**: sorting order (default: "desc")

     Example:
     - Website: `/?f=2&c=1_2&q=Sword+Art+Online&s=seeders&o=desc`
     - API:     `/api/v1/nyaa?filter=2&category=1&subcategory=2&query=Sword+Art+Online&sort=seeders&order=desc`


     All parameters are optional.

     Supported values for all the parameters are same as the website.

     Only difference is parameter names are not abbreviated.
    """
    return await nyaa.search(
        keyword=query,
        category=category,
        subcategory=subcategory,
        page=page,
        filter=filter,
        sort=sort,
        order=order
    )


@router.get(
    path="/view/{view_id}",
    response_model=TorrentResponse
)
async def nyaa_view(view_id: int):
    """
     View details torrent
     - **view_id**: required
    """
    return await nyaa.view(view_id)
