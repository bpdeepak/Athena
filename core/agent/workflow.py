from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes import planner_node, researcher_node, alerter_node, responder_node, executor_node
import logging

logger = logging.getLogger(__name__)

def route_human_gate(state: AgentState):
    """Routing function to conditionally ask for human approval."""
    if state.get("requires_approval") and not state.get("approved"):
        logger.info("Human approval required. Stopping workflow.")
        return END
    return "executor"

builder = StateGraph(AgentState)

# Add nodes
builder.add_node("planner", planner_node)
builder.add_node("researcher", researcher_node)
builder.add_node("alerter", alerter_node)
builder.add_node("responder", responder_node)
builder.add_node("executor", executor_node)

# Define edges
builder.set_entry_point("planner")
builder.add_edge("planner", "researcher")
builder.add_edge("researcher", "alerter")
builder.add_edge("alerter", "responder")

# Conditional edge from responder to executor (human-in-the-loop gate)
builder.add_conditional_edges("responder", route_human_gate)

# Edge from executor to end
builder.add_edge("executor", END)

# Compile graph
graph = builder.compile()

def process_event(event_payload: dict):
    """Entry point to process a webhook event through the agent."""
    initial_state = {
        "event_payload": event_payload,
        "plan": [],
        "research_context": "",
        "identified_risks": [],
        "draft_response": "",
        "requires_approval": False,
        "approved": False,
        "action_log": [],
        "error": None
    }
    
    logger.info(f"Starting agent workflow for event: {event_payload.get('event_type')}")
    # Run the graph
    # By default, config checkpointer could be added here for resumption
    final_state = graph.invoke(initial_state)
    logger.info(f"Workflow finished. Final node: {final_state.get('current_node')}")
    return final_state
