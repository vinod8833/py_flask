from flask import Flask, request, jsonify
from bson import json_util
import json




from pymongo import MongoClient

# Flask app object
app = Flask(__name__)

# Set up MongoDB connection
client = MongoClient('mongodb+srv://vinod:vinod8833@cluster0.prvvdcz.mongodb.net/?retryWrites=true&w=majority')
db = client['college']
student_collection = db['student'] # collection is called table


@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/vinod')
def hello_vinod():
	return 'Hello, Vinod!'

@app.route('/student', methods=['POST'])
def add_data():
	data = request.json

	# Insert data into MongoDB
	student_collection.insert_one(data)

	return 'Data added to MongoDB'

@app.route('/students', methods=['GET'])
def get_all_students():
    students = list(student_collection.find())
    return jsonify(json.loads(json_util.dumps(students)))


@app.route('/student/<int:roll_no>', methods=['GET'])
def get_single_student(roll_no):
    student = student_collection.find_one({"roll_no": roll_no})
    if student:
        return jsonify(json.loads(json_util.dumps(student)))
    else:
        return "Student not found", 404


@app.route('/student/<int:roll_no>', methods=['DELETE'])
def delete_student(roll_no):
    result = student_collection.delete_one({"roll_no": roll_no})
    if result.deleted_count > 0:
        return "Student deleted", 200
    else:
        return "Student not found", 404


@app.route('/student/<int:roll_no>', methods=['PUT', 'PATCH'])
def update_student(roll_no):
    data = request.json
    result = student_collection.update_one(
        {"roll_no": roll_no},
        {"$set": data}
    )
    
    if result.modified_count > 0:
        return "Student updated", 200
    else:
        return "Student not found", 404





if __name__ == '__main__':
	app.run()
