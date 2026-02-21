from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any, Dict
from datetime import datetime
from database import (
    RoleEnum, EpicStatusEnum, RagStatusEnum, StoryStatusEnum, 
    PriorityEnum, RiskSeverityEnum, RiskStatusEnum
)

class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: RoleEnum

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: str
    perf_score: int
    created_at: datetime
    class Config:
        from_attributes = True

class EpicBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: EpicStatusEnum = EpicStatusEnum.OPEN

class EpicCreate(EpicBase):
    id: str # e.g. EPIC-1

class EpicOut(EpicBase):
    id: str
    rag_status: RagStatusEnum
    created_at: datetime
    class Config:
        from_attributes = True

class StoryBase(BaseModel):
    title: str
    description: Optional[str] = None
    epic_id: Optional[str] = None
    assignee_id: Optional[str] = None
    status: StoryStatusEnum = StoryStatusEnum.TODO
    priority: PriorityEnum = PriorityEnum.MEDIUM
    points: Optional[int] = None
    blocked_by: Optional[List[str]] = []

class StoryCreate(StoryBase):
    id: str # e.g. STORY-1

class StoryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    epic_id: Optional[str] = None
    assignee_id: Optional[str] = None
    status: Optional[StoryStatusEnum] = None
    priority: Optional[PriorityEnum] = None
    points: Optional[int] = None
    blocked_by: Optional[List[str]] = None
    chaos_flag: Optional[bool] = None

class StoryOut(StoryBase):
    id: str
    chaos_flag: bool
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class RiskBase(BaseModel):
    story_id: Optional[str] = None
    severity: RiskSeverityEnum
    description: str
    status: RiskStatusEnum = RiskStatusEnum.OPEN
    reported_by: Optional[str] = None

class RiskCreate(RiskBase):
    pass

class RiskOut(RiskBase):
    id: str
    created_at: datetime
    class Config:
        from_attributes = True
