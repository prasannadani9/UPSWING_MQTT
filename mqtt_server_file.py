import pika
import pymongo
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["prasannadb"]
collection = db["PrasannasCollection"]

broker = 'localhost'
port = 5672
queue_name = "status_zero_to_six"

def connect_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=broker, port=port))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    return connection, channel

class TimeRange(BaseModel):
    start_time: datetime
    end_time: datetime

@app.post("/status")
def get_status_count(time_range: TimeRange):
    pipeline = [
        {"$match": {"timestamp": {"$gte": time_range.start_time, "$lte": time_range.end_time}}},
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]
    result = list(collection.aggregate(pipeline))
    return {item["_id"]: item["count"] for item in result}

def callback(ch, method, properties, body):
    status = int(body)
    doc = {"status": status, "timestamp": datetime.now()}
    collection.insert_one(doc)
    print(f"Inserted {doc}")
    

if __name__ == "__main__":
    connection, channel = connect_rabbitmq()
    channel.basic_consume(queue='statuses', on_message_callback=callback, auto_ack=True)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Interrupted")
    finally:
        connection.close()
