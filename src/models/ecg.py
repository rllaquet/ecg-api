"""Database model for ECGs."""
import pendulum
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pymongo.database import Database

from schemas.ecg import LeadOut, EcgOut
from schemas.users import User


async def create_ecg(db: Database, user: User, leads: list[LeadOut]) -> str:
    """Create a new ECG entry.

    Args:
        db: instance of MongoDB database.
        user: User making the request.
        leads: list of the ECG's leads.

    Returns:
        ObjectId: inserted ECG id.
    """
    record = await db.ecg.insert_one(
        {
            "created_at": pendulum.now(),
            "leads": jsonable_encoder(leads),
            "user": ObjectId(user.id),
        }
    )
    return str(record.inserted_id)


async def find_ecg(db: Database, user: User, ecg_id: ObjectId) -> EcgOut | None:
    """Get a single ECG entry by id.

    Args:
        db: instance of MongoDB database.
        user: User making the request.
        ecg_id: id of the ECG to be fetched.

    Returns:
        EcgOut: ECG object.
    """
    ecg = await db.ecg.find_one({"_id": ecg_id, "user": ObjectId(user.id)})
    if ecg:
        return EcgOut(id=str(ecg["_id"]), date=ecg["created_at"], leads=ecg["leads"])
    return None
