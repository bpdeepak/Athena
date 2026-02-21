from fastapi import FastAPI, BackgroundTasks, Request
import logging
from graph_syncer import GraphSyncer
from vector_indexer import VectorIndexer
# We will import agent later once implemented

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AthenaCore")

app = FastAPI(title="Athena Core - Agent Brain API")

graph_syncer = GraphSyncer()
vector_indexer = VectorIndexer()

@app.on_event("shutdown")
def shutdown_event():
    graph_syncer.close()

@app.get("/health")
def read_health():
    return {"status": "ok", "service": "athena-core"}

@app.post("/api/v1/webhook/event")
async def receive_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    logger.info(f"Received webhook: {payload.get('event_type')} for {payload.get('entity_type')} {payload.get('entity_id')}")
    
    event_type = payload.get("event_type")
    entity_type = payload.get("entity_type")
    entity_id = payload.get("entity_id")
    changed_fields = payload.get("changed_fields", {})
    
    # Run syncers in background
    background_tasks.add_task(graph_syncer.sync_entity, event_type, entity_type, entity_id, changed_fields)
    background_tasks.add_task(vector_indexer.sync_entity, event_type, entity_type, entity_id, changed_fields)
    
    # Here we would also trigger the LangGraph agent if the event requires action
    # e.g., if a risk becomes critical, or a milestone is delayed
    # background_tasks.add_task(trigger_agent_workflow, payload)
    
    return {"status": "accepted"}
