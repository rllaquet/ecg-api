from datetime import datetime

from pydantic import BaseModel


class LeadBase(BaseModel):
    name: str
    n_samples: int | None = None
    signal: list[int]


class LeadOut(LeadBase):
    zero_crossings: int


class EcgBase(BaseModel):
    leads: list[LeadBase]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "leads": [
                        {"name": "I", "n_samples": 3, "signal": [1, 2, 3]},
                        {"name": "II", "signal": [1, 0, -1]},
                    ]
                },
            ]
        }
    }


class EcgOut(EcgBase):
    id: str
    date: datetime
    leads: list[LeadOut]
