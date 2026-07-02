import os
import cognee
from dotenv import load_dotenv

load_dotenv()

COGNEE_URL = "https://tenant-cd3bc089-a188-4774-82c6-7f276c2cd16f.aws.cognee.ai"
COGNEE_API_KEY = os.getenv("COGNEE_API_KEY")

async def remember_message(user_id: int, message: str):
    await cognee.serve(url=COGNEE_URL, api_key=COGNEE_API_KEY)
    await cognee.remember(message, dataset_name=f"user_{user_id}")
    await cognee.disconnect()

async def recall_memories(user_id: int, query: str) -> list:
    await cognee.serve(url=COGNEE_URL, api_key=COGNEE_API_KEY)
    results = await cognee.recall(query, datasets=[f"user_{user_id}"])
    await cognee.disconnect()
    
    memories = []
    for result in results:
        if result.get("text"):
            memories.append({
                "type": "cognee_insight",
                "value": result["text"]
            })
    return memories