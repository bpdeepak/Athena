from agent.state import AgentState
from llm_provider import get_llm_provider
from agent.tools import query_graph_database, search_vector_database, take_sim_action
from langchain_core.messages import SystemMessage, HumanMessage
import json

provider = get_llm_provider()
llm = provider.get_chat_model()

# Bind tools if supported, otherwise just use as regular prompts (for Ollama fallback simplicity)
# Langchain ChatOllama supports tools, but let's keep prompting explicit if needed.
llm_with_tools = llm.bind_tools([query_graph_database, search_vector_database, take_sim_action])

def planner_node(state: AgentState):
    """Analyzes the event and plans research steps."""
    event = state.get("event_payload", {})
    prompt = f"""You are the Planner Agent. Analyze this event: {json.dumps(event)}
    What needs to be researched? Output a JSON list of steps. Nothing else."""
    
    # Quick mock implementation for speed, normally we'd parse LLM output
    response = llm.invoke([HumanMessage(content=prompt)])
    # For robust parsing:
    try:
        plan = json.loads(response.content)
        if not isinstance(plan, list): plan = ["Analyze entity impact"]
    except:
        plan = ["Identify related entities via Graph", "Check context via VectorDB"]
        
    return {"plan": plan, "current_node": "planner"}

def researcher_node(state: AgentState):
    """Executes research tools based on the plan."""
    plan = state.get("plan", [])
    event = state.get("event_payload", {})
    
    # We will invoke the agent with tools to gather context
    prompt = f"Plan: {plan}. Event: {event}. Use tools to gather full context around this event."
    response = llm_with_tools.invoke([HumanMessage(content=prompt)])
    
    # If it called tools, we execute them and get context. Simplified here to just show flow.
    # A real implementation would loop through tool calls.
    context = ""
    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"] == "query_graph_database":
                context += query_graph_database.invoke(tool_call["args"])
            elif tool_call["name"] == "search_vector_database":
                context += search_vector_database.invoke(tool_call["args"])
                
    return {"research_context": context, "current_node": "researcher"}

def alerter_node(state: AgentState):
    """Identifies risks based on the research context."""
    context = state.get("research_context", "")
    prompt = f"Based on this context: {context}, identify any risks. Return JSON array of dicts with 'risk' and 'severity'."
    
    response = llm.invoke([HumanMessage(content=prompt)])
    try:
        risks = json.loads(response.content)
        if not isinstance(risks, list): risks = [{"risk": "Unknown", "severity": "MEDIUM"}]
    except:
        risks = [{"risk": "Detected potential issue from context", "severity": "MEDIUM"}]
        
    return {"identified_risks": risks, "current_node": "alerter"}

def responder_node(state: AgentState):
    """Drafts a response or action plan."""
    risks = state.get("identified_risks", [])
    prompt = f"Risks identified: {risks}. Draft an action plan to mitigate these."
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    # Determine if approval is needed (e.g., if there are CRITICAL risks)
    requires_approval = any(r.get("severity", "").upper() == "CRITICAL" for r in risks)
    
    return {
        "draft_response": response.content, 
        "requires_approval": requires_approval,
        "current_node": "responder"
    }

def executor_node(state: AgentState):
    """Executes the approved action plan."""
    if state.get("requires_approval") and not state.get("approved"):
        return {"action_log": ["Action blocked: Pending human approval."], "current_node": "executor"}
        
    response = state.get("draft_response", "")
    # In a full impl, we'd use `take_sim_action` tool here based on the draft_response
    
    from atl import log_action
    log_action("EXECUTION", f"Executed mitigation plan: {response[:50]}...")
    
    return {"action_log": [f"Executed: {response}"], "current_node": "executor"}
