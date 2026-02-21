from typing import TypedDict, Annotated, List, Any, Optional
import operator

class AgentState(TypedDict):
    # Core inputs
    event_payload: dict
    
    # Internal reasoning state
    plan: List[str]
    research_context: str
    identified_risks: List[dict]
    draft_response: str
    
    # Human-in-the-loop
    requires_approval: bool
    approved: bool
    
    # Execution
    action_log: List[str]
    
    # Graph routing
    current_node: str
    error: Optional[str]
