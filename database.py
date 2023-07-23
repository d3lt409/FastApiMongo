"""
['aggregate', 'aggregate_raw_batches', 'bulk_write', 'codec_options', 'count_documents', 'create_index', 'create_indexes', 'database', 'delegate', 'delete_many', 'delete_one', 'distinct', 'drop', 'drop_index', 'drop_indexes', 'estimated_document_count', 'find', 'find_one', 'find_one_and_delete', 'find_one_and_replace', 'find_one_and_update', 'find_raw_batches', 'full_name', 'get_io_loop', 'index_information', 'insert_many', 'insert_one', 'list_indexes', 'name', 'options', 'read_concern', 'read_preference', 'rename', 'replace_one', 'update_many', 'update_one', 'watch', 'with_options', 'wrap', 'write_concern']
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from pymongo.cursor import  Cursor

from models.models import PyObjectId, Task
from bson.objectid import ObjectId
import bson


client:AsyncIOMotorClient = AsyncIOMotorClient("mongodb://localhost:27017")
database:AsyncIOMotorDatabase = client.taskdatabase
collection:AsyncIOMotorCollection = database.tasks


async def get_task_id(id):
    try:
        _id = ObjectId(id)
        task = await collection.find_one({"_id": _id})
        if task:
            task["_id"] = str(task["_id"])
            return Task(**task)
    except bson.errors.InvalidId:
        return None
    

async def get_task_title(title):
    task = await collection.find_one({"title": title})
    return task

async def get_all_tasks():
    cursor:Cursor = collection.find({})
    tasks = await cursor.to_list(length=None)
    all_tasks = []
    for task in tasks:
        new_task = task
        new_task["_id"] = str(new_task["_id"])
        all_tasks.append(new_task)
    return [Task(**task) for task in all_tasks]

async def create_new_task(task):
    new_task = await collection.insert_one(task)
    created_tasks = await collection.find_one({'_id': new_task.inserted_id})
    created_tasks["_id"] = str(new_task.inserted_id)
    print(Task(**created_tasks))
    return Task(**created_tasks)

async def update_task_id(task_id, task):
    task = { k:v for k,v in task.items() if v}
    await collection.update_one({"_id": ObjectId(task_id)}, {"$set": task})
    updated_task = await collection.find_one({"_id": ObjectId(task_id)})
    if updated_task:
        updated_task["_id"] = str(updated_task["_id"])
        return Task(**updated_task)

async def delete_task_id(task_id):
    await collection.delete_one({"_id": ObjectId(task_id)})
    return True