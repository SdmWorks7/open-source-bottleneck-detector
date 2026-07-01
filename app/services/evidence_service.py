def memories_to_evidence(memories: list) -> list:
    evidence = []
    for memory in memories:
        evidence.append({
            "category": memory["type"],
            "item": memory["value"],
            "score": 5,
            "source": "user_memory"
        })
    return evidence

def github_to_evidence(events: list)-> list:
    push_count= sum(1 for event in events if event["type"]=="PushEvent")

    if push_count == 0:
        return []
    elif push_count <= 5:
        score = 4
    elif push_count <= 20:
        score = 6
    else:
        score = 9

    return [{
         "category": "activity",
        "item": "git",
        "score": score,
        "source": "github"
    }]

def generate_evidence(memories: list, github_events: list) -> list:
    evidence = []
    evidence.extend(memories_to_evidence(memories))
    evidence.extend(github_to_evidence(github_events))
    return evidence



