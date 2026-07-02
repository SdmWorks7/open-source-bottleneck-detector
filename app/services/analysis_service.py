from app.services.cognee_service import recall_memories
from app.services.github_service import get_github_username, fetch_github_events
from app.services.evidence_service import generate_evidence
from app.services.bottleneck_service import rank_bottlenecks
from app.services.llm_service import generate_explanation
from app.services.report_service import save_report

async def run_analysis(user_id: int) -> dict:
    memories = await recall_memories(user_id, "skills, weaknesses and goals")
    
    github_username = await get_github_username(user_id)
    if github_username:
        events = await fetch_github_events(github_username)
    else:
        events = []
    
    evidence = generate_evidence(memories, events)
    bottlenecks = rank_bottlenecks(evidence)
    explanation = generate_explanation(bottlenecks)
    
    report = {
    "user_id": user_id,
    "bottlenecks": bottlenecks,
    "explanation": explanation
    }

    r_id = await save_report(user_id, report)

    return {**report, "report_id": r_id}