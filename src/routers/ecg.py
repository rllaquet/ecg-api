from bson import ObjectId
from fastapi import APIRouter, Depends, Path, HTTPException, status
from pymongo.database import Database

from dependencies import get_db, get_current_user
from models.ecg import create_ecg, find_ecg
from schemas.ecg import EcgBase, LeadOut, EcgOut
from schemas.users import User
from utils.ecg_tools import zero_crossings

router = APIRouter(
    prefix="/ecg",
    dependencies=[Depends(get_current_user)],
)


def valid_ecg_id(ecg_id: str = Path(...)) -> ObjectId:
    """Validates that ecg_id is a valid ObjectId and returns it."""
    try:
        ecg_id = ObjectId(ecg_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Incorrect ECG id format. It should be valid ObjectId.",
        )

    return ecg_id


@router.post("", response_description="Create a new ECG entry.", status_code=201)
async def post_ecg(
    ecg: EcgBase,
    db: Database = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> str:
    """Adds a new ECG entry to the database."""
    leads = []

    for lead in ecg.leads:
        lead = LeadOut(**lead.model_dump(), zero_crossings=zero_crossings(lead.signal))
        lead.n_samples = len(lead.signal)
        leads.append(lead)

    ecg_id = await create_ecg(db, current_user, leads)
    return ecg_id


@router.get(
    "/{ecg_id}",
    response_description="Get a single ECG entry by id.",
    responses={404: {"description": "ECG not found"}},
)
async def get_ecg(
    ecg_id: ObjectId = Depends(valid_ecg_id),
    db: Database = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> EcgOut:
    """Returns a single ECG entry by id."""
    ecg = await find_ecg(db, current_user, ecg_id)
    if not ecg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ECG not found"
        )
    return ecg
