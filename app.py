from flask import Flask, Response, request, render_template, jsonify
import json
from bson import json_util
from pymongo import MongoClient

app=Flask(__name__)  

try:
    mongo = MongoClient("mongodb+srv://user:user@cluster0.ucjlkjw.mongodb.net/")
    print(mongo)
    db = mongo.ADBCoding 
    mongo.server_info() 
except Exception as e:
    print("Error while connecting to db"+str(e))
    
@app.route("/")
def home():
    return "<h1>Welcome To Home Page</h1>"

@app.route('/netflix', methods=['POST'])
def DataInsertion():
  try:
    data = request.get_json()
    dbResponse = db.netflix.insert_one(data)
    response = Response("New Record is successfully added in netflix data file",status=201,mimetype='application/json')
    return response
  except Exception as ex:
    response = Response("Error while inserting new record in netflix data file!!",status=500,mimetype='application/json')
    return response 

@app.route('/netflix', methods=['GET'])
def DataRetrival():
  try:
    documents = db.netflix.find()
    output = [{item: data[item] for item in data if item != '_id'} for data in documents]
    return jsonify(output)
  except Exception as ex:
    response = Response("Error while searching new record!!",status=500,mimetype='application/json')
    return response

@app.route('/netflix/<string:fname>', methods=['GET'])
def RetriveOneRecord(fname):
  try:
    document = db.netflix.find_one({"title":fname})
    print(document)
    if document:
        return json.loads(json_util.dumps(document))
    else:
        return jsonify({"message": "Document not found"}), 404
  except Exception as ex:
    response = Response("Search Record Error!!"+str(ex),status=500,mimetype='application/json')
    return response

@app.route('/netflix/<string:fname>', methods=['DELETE'])
def DeleteRecordByTitle(fname):
  try:
    result= db.netflix.delete_one({"title":fname})
    if result.deleted_count == 1:
        response = Response("Document Deleted Successfully!",status=200,mimetype='application/json')
    else:
        response = Response("Document not found or not deleted !",status=200,mimetype='application/json')
    return response
  except Exception as ex:
    response = Response("Error while Deleting a Record!!",status=500,mimetype='application/json')
    return response

@app.route('/netflix/<string:fname>', methods=['PATCH'])
def UpdateRecordByTitle(fname):
    
    try:
        document = db.netflix.find_one({"title": fname})
        if document is None:
            return jsonify({"message": "Document not found"}), 404

        update_data = request.json
        for key, value in update_data.items():
            if key in ['id','title','description','runtime','imdb_score']:
                document[key] = value

        db.netflix.update_one({"title":fname}, {"$set": document})

        return jsonify({"message": "Document updated successfully"})
    except Exception as ex:
        response = Response("Error While Updating New Record!!",status=500,mimetype='application/json')
    return response
    

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)

