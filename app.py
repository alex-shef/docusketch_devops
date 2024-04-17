from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from datetime import datetime
import yappi
import atexit


# End profiling and save the results into file
def output_profiler_stats_file():
    profile_file_name = 'yappi.' + datetime.now().isoformat()
    func_stats = yappi.get_func_stats()
    func_stats.save(profile_file_name, type='pstat')
    yappi.stop()
    yappi.clear_stats()


yappi.start()
atexit.register(output_profiler_stats_file)


app = Flask(__name__)

client = MongoClient("mongodb://mongodb:27017/")
db = client["mydatabase"]
collection = db["mycollection"]

# Creating a uniqueness index for the "key" field
collection.create_index([("key", 1)], unique=True)


@app.route('/', methods=['GET'])
def hello():
    return "Hello, Docusketch!"


@app.route('/api/keyvalue', methods=['POST'])
def create_key_value():
    data = request.json
    key = data.get("key")
    value = data.get("value")
    if key and value:
        try:
            collection.insert_one({"key": key, "value": value})
            return jsonify({"message": "Key-Value pair created successfully"}), 201
        except DuplicateKeyError:
            return jsonify({"error": "Key already exists"}), 409
    else:
        return jsonify({"error": "Invalid request. Key and value are required."}), 400


@app.route('/api/keyvalue/<key>', methods=['PUT'])
def update_key_value(key):
    data = request.json
    new_value = data.get("value")
    if new_value:
        collection.update_one({"key": key}, {"$set": {"value": new_value}})
        return jsonify({"message": "Key-Value pair updated successfully"}), 200
    else:
        return jsonify({"error": "Invalid request. New value is required."}), 400


@app.route('/api/keyvalue/<key>', methods=['GET'])
def get_key_value(key):
    document = collection.find_one({"key": key})
    if document:
        return jsonify({"key": document["key"], "value": document["value"]}), 200
    else:
        return jsonify({"error": "Key not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
