import os
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean, Enum as SQLEnum, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.types import TypeDecorator, VARCHAR
import enum
import uuid

DB_PATH = os.getenv("DB_PATH", "simulator.db")
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class JSONType(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

class RoleEnum(str, enum.Enum):
    DEV = "DEV"
    PM = "PM"
    QA = "QA"
    VP = "VP"

class EpicStatusEnum(str, enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class RagStatusEnum(str, enum.Enum):
    RED = "RED"
    AMBER = "AMBER"
    GREEN = "GREEN"

class StoryStatusEnum(str, enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    REVIEW = "REVIEW"
    DONE = "DONE"
    BLOCKED = "BLOCKED"

class PriorityEnum(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class RiskSeverityEnum(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class RiskStatusEnum(str, enum.Enum):
    OPEN = "OPEN"
    MITIGATING = "MITIGATING"
    CLOSED = "CLOSED"

class EntityTypeEnum(str, enum.Enum):
    STORY = "STORY"
    EPIC = "EPIC"
    RISK = "RISK"
    USER = "USER"
    SPRINT = "SPRINT"
    MILESTONE = "MILESTONE"

class ChangeTypeEnum(str, enum.Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(SQLEnum(RoleEnum), nullable=False)
    perf_score = Column(Integer, default=50)
    created_at = Column(DateTime, default=datetime.utcnow)

class Epic(Base):
    __tablename__ = "epics"
    id = Column(String(20), primary_key=True)
    title = Column(Text, nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(EpicStatusEnum), nullable=False, default=EpicStatusEnum.OPEN)
    rag_status = Column(SQLEnum(RagStatusEnum), default=RagStatusEnum.GREEN)
    created_at = Column(DateTime, default=datetime.utcnow)

class Story(Base):
    __tablename__ = "stories"
    id = Column(String(20), primary_key=True)
    epic_id = Column(String(20), ForeignKey("epics.id"))
    assignee_id = Column(String, ForeignKey("users.id"))
    title = Column(Text, nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(StoryStatusEnum), nullable=False, default=StoryStatusEnum.TODO)
    priority = Column(SQLEnum(PriorityEnum), nullable=False, default=PriorityEnum.MEDIUM)
    points = Column(Integer)
    blocked_by = Column(JSONType) # Array of Story IDs
    chaos_flag = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    epic = relationship("Epic")
    assignee = relationship("User")

class Risk(Base):
    __tablename__ = "risks"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id = Column(String(20), ForeignKey("stories.id"))
    severity = Column(SQLEnum(RiskSeverityEnum), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(SQLEnum(RiskStatusEnum), nullable=False, default=RiskStatusEnum.OPEN)
    reported_by = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_log"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    entity_type = Column(SQLEnum(EntityTypeEnum), nullable=False)
    entity_id = Column(String(50), nullable=False)
    change_type = Column(SQLEnum(ChangeTypeEnum), nullable=False)
    payload = Column(JSONType, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
