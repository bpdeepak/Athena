import pprint
from agent.workflow import process_event

def test_workflow():
    print("Testing LangGraph Workflow...")
    
    sample_event = {
        "event_type": "risk:created",
        "entity_type": "RISK",
        "entity_id": "r-123",
        "changed_fields": {
            "severity": "CRITICAL",
            "description": "API Gateway is failing under load."
        },
        "source": "system"
    }
    
    # Normally this hits the real LLM, Graph, and VectorDB.
    # Without API keys or a local Ollama running, it will fail gracefully or output errors to logs.
    try:
        final_state = process_event(sample_event)
        print("Final Agent State:")
        pprint.pprint(final_state)
    except Exception as e:
        print(f"Workflow test failed (likely missing LLM API keys or local DBs): {e}")

if __name__ == "__main__":
    test_workflow()
