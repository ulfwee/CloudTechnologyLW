import os
from datetime import datetime, timezone

from azure.cosmos import CosmosClient
from dotenv import load_dotenv

load_dotenv()

endpoint = os.environ["COSMOS_ENDPOINT"]
key = os.environ["COSMOS_KEY"]
database_name = os.getenv("COSMOS_DATABASE", "course-db")
container_name = os.getenv("COSMOS_CONTAINER", "products")
student_id = os.getenv("STUDENT_ID", "student-001")

client = CosmosClient(endpoint, credential=key)
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

item = {
    "id": "p-python-001",
    "studentId": student_id,
    "name": "Python-created item",
    "category": "software",
    "price": 20.0,
    "inStock": True,
    "tags": ["python", "azure"],
    "createdAt": datetime.now(timezone.utc).isoformat(),
}

container.upsert_item(item)
print("UPSERT:", item["id"])

stored = container.read_item(
    item=item["id"],
    partition_key=student_id,
)
print("POINT READ:", stored["name"], stored["price"])

query = """
SELECT c.id, c.name, c.price
FROM c
WHERE c.studentId = @studentId AND c.price >= @minPrice
ORDER BY c.price DESC
"""

parameters = [
    {"name": "@studentId", "value": student_id},
    {"name": "@minPrice", "value": 20},
]

for row in container.query_items(
    query=query,
    parameters=parameters,
    partition_key=student_id,
):
    print("QUERY:", row)