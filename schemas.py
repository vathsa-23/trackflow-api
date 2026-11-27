from typing import Literal
from pydantic import BaseModel, Field

ApplicationStatus = Literal["Applied", "Interviewing", "Offer", "Rejected"]


class ApplicationCreate(BaseModel):
    company: str = Field(..., min_length=1, max_length=100)
    role: str = Field(..., min_length=1, max_length=100)
    status: ApplicationStatus = "Applied"
    location: str = Field(default="Hyderabad", max_length=100)
    notes: str = Field(default="", max_length=500)


class ApplicationUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=100)
    role: str | None = Field(default=None, min_length=1, max_length=100)
    status: ApplicationStatus | None = None
    location: str | None = Field(default=None, max_length=100)
    notes: str | None = Field(default=None, max_length=500)


class ApplicationResponse(BaseModel):
    id: int
    company: str
    role: str
    status: ApplicationStatus
    location: str
    notes: str
    created_at: str