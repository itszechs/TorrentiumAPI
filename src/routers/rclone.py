from typing import List

from fastapi import APIRouter

from src.modules.rclone.model import TransferResponse
from src.modules.rclone.rclone_rc import RcloneRC

rclone = RcloneRC()

router = APIRouter(
    prefix="/api/v1/rclone",
    tags=["Rclone"]
)


@router.get(
    path="/transfers",
    response_model=List[TransferResponse]
)
async def get_transfers():
    """
    Get all transfers
    """
    transfers = []
    for transfer in rclone.stats():
        transfers.append(
            TransferResponse(
                name=transfer.name,
                size=transfer.size,
                bytes=transfer.bytes,
                speed=transfer.speed,
                percentage=transfer.percentage,
                eta=transfer.eta,
                group=transfer.group,
                size_human=transfer.size_human,
                bytes_human=transfer.bytes_human,
                progress=transfer.progress,
                speed_human=transfer.speed_human,
                eta_human=transfer.eta_human
            )
        )
    return transfers
