import azure.functions as func
import pymongo
import json
from bson.json_util import dumps

def main(req: func.HttpRequest) -> func.HttpResponse:

    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    if not data:
        return func.HttpResponse("Empty request body", status_code=400)

    try:
        client = pymongo.MongoClient("mongodb://secondprojectcosmo:bVSfqyIJWu6ZmMd1uTXwUra16vQimxVWVJFQ1VSJ1inrJ5UyrEiYu2JRKTtBbPp5cZdJwhx70zIuACDbWbyfkA==@secondprojectcosmo.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@secondprojectcosmo@")
        db = client["secondprojectdatabase"]
        collection = db["advertisements"]

        result = collection.insert_one(data)

        # Fetch inserted document
        inserted_doc = collection.find_one(
            {"_id": result.inserted_id}
        )

        return func.HttpResponse(
            dumps(inserted_doc),
            mimetype="application/json",
            status_code=201
        )

    except Exception as e:
        return func.HttpResponse(
            f"Database error: {str(e)}",
            status_code=500
        )
