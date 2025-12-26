import azure.functions as func
import pymongo
from bson.objectid import ObjectId


def main(req: func.HttpRequest) -> func.HttpResponse:

    id = req.params.get('id')

    if not id:
        return func.HttpResponse(
            "Please pass an id in the query string",
            status_code=400
        )

    try:
        client = pymongo.MongoClient("mongodb://secondprojectcosmo:bVSfqyIJWu6ZmMd1uTXwUra16vQimxVWVJFQ1VSJ1inrJ5UyrEiYu2JRKTtBbPp5cZdJwhx70zIuACDbWbyfkA==@secondprojectcosmo.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@secondprojectcosmo@")
        database = client["secondprojectdatabase"]
        collection = database["advertisements"]

        # ✅ Convert string → ObjectId
        query = {"_id": id }
        print("Query being sent to MongoDB:", query)

        result = collection.delete_one(query)

        if result.deleted_count == 1:
            return func.HttpResponse(
                "Advertisement deleted successfully",
                status_code=200
            )
        else:
            return func.HttpResponse(
                "Advertisement not found",
                status_code=404
            )

    except Exception as e:
        print("Delete failed:", str(e))
        return func.HttpResponse(
            "Invalid id format or database error",
            status_code=400
        )
