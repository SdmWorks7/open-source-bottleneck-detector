def rank_bottlenecks(evidence: list) -> list:
    scores = {}
    counts = {}
    categories = {}
    sources = {}

    for item in evidence:
        key = item["item"]
        if item["category"] == "weakness":
            severity = item["score"]
        else:
            severity = 10 - item["score"]

        if key not in scores:
            scores[key] = 0
            counts[key] = 0
            categories[key] = item["category"]
            sources[key] = []

        scores[key] += severity
        counts[key] += 1
        sources[key].append(item["source"])

    bottlenecks = []
    for key in scores:
        avg_severity = round(scores[key] / counts[key], 1)
        bottlenecks.append({
            "item": key,
            "category": categories[key],
            "severity": avg_severity,
            "sources": sources[key]
        })

    bottlenecks.sort(key=lambda x: x["severity"], reverse=True)
    return bottlenecks