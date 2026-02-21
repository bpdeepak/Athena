from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import database
import schemas
from database import engine, SessionLocal
from webhook_dispatcher import dispatch_webhook
import uuid

database.init_db()

app = FastAPI(title="Project Universe - Mock Jira API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def read_health():
    return {"status": "ok"}

# --- USERS ---
@app.post("/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = database.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users", response_model=List[schemas.UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(database.User).offset(skip).limit(limit).all()
    return users

# --- EPICS ---
@app.post("/epics", response_model=schemas.EpicOut)
def create_epic(epic: schemas.EpicCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_epic = database.Epic(**epic.model_dump())
    db.add(db_epic)
    db.commit()
    db.refresh(db_epic)
    
    background_tasks.add_task(
        dispatch_webhook,
        event_type="epic:created",
        entity_type="EPIC",
        entity_id=db_epic.id,
        changed_fields={"title": db_epic.title, "status": db_epic.status.value},
        source="system"
    )
    return db_epic

@app.get("/epics", response_model=List[schemas.EpicOut])
def read_epics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(database.Epic).offset(skip).limit(limit).all()

# --- STORIES ---
@app.post("/stories", response_model=schemas.StoryOut)
def create_story(story: schemas.StoryCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_story = database.Story(**story.model_dump())
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    
    background_tasks.add_task(
        dispatch_webhook,
        event_type="story:created",
        entity_type="STORY",
        entity_id=db_story.id,
        changed_fields={"title": db_story.title, "status": db_story.status.value, "epic_id": db_story.epic_id},
        source="system"
    )
    return db_story

@app.get("/stories", response_model=List[schemas.StoryOut])
def read_stories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(database.Story).offset(skip).limit(limit).all()

@app.put("/stories/{story_id}", response_model=schemas.StoryOut)
def update_story(story_id: str, story_update: schemas.StoryUpdate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_story = db.query(database.Story).filter(database.Story.id == story_id).first()
    if not db_story:
        raise HTTPException(status_code=404, detail="Story not found")
        
    update_data = story_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_story, key, value)
        
    db.commit()
    db.refresh(db_story)
    
    background_tasks.add_task(
        dispatch_webhook,
        event_type="story:updated",
        entity_type="STORY",
        entity_id=db_story.id,
        changed_fields=update_data,
        source="system"
    )
    return db_story

# --- RISKS ---
@app.post("/risks", response_model=schemas.RiskOut)
def create_risk(risk: schemas.RiskCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_risk = database.Risk(**risk.model_dump())
    db.add(db_risk)
    db.commit()
    db.refresh(db_risk)
    
    background_tasks.add_task(
        dispatch_webhook,
        event_type="risk:created",
        entity_type="RISK",
        entity_id=db_risk.id,
        changed_fields={"severity": db_risk.severity.value, "description": db_risk.description, "status": db_risk.status.value},
        source="system"
    )
    return db_risk

@app.get("/risks", response_model=List[schemas.RiskOut])
def read_risks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(database.Risk).offset(skip).limit(limit).all()

@app.put("/risks/{risk_id}", response_model=schemas.RiskOut)
def update_risk(risk_id: str, risk_update: schemas.RiskBase, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_risk = db.query(database.Risk).filter(database.Risk.id == risk_id).first()
    if not db_risk:
        raise HTTPException(status_code=404, detail="Risk not found")
        
    update_data = risk_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_risk, key, value)
        
    db.commit()
    db.refresh(db_risk)
    
    background_tasks.add_task(
        dispatch_webhook,
        event_type="risk:updated",
        entity_type="RISK",
        entity_id=db_risk.id,
        changed_fields=update_data,
        source="system"
    )
    return db_risk
