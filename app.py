from flask import Flask,jsonify,request
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash,check_password_hash
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
client = MongoClient("mongodb://localhost:27017")
db = client["motel"]
collection = db["types"]

@app.route('/register',methods=['POST'])
def addemail():
      data = request.get_json()


      if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "All fields are required"}), 400

      if collection.find_one({"email": data["email"]}):  
          return jsonify({"error": "Email already registered"}), 400


      hashed_password = generate_password_hash(data["password"])

      userdata = {
         "username": data["username"],
        "email": data["email"],
        "password": hashed_password
      }
      result = collection.insert_one(userdata)
      return jsonify({"id": str(result.inserted_id), "message": "User registered successfully"}), 201


@app.route('/Login',methods=['POST'])
def loginid ():
      
        data = request.get_json()
        if not data.get("email") or not data.get("password"):
          return jsonify({"error": " email and password are required"}),400

        user = collection.find_one({"email": data["email"]})
        if not user:
          return jsonify({"error": "Invalid email or password"}), 401

        if not check_password_hash(user["password"], data["password"]):
          return jsonify({"error": "Invalid email or password"}), 401

        user_data = {
            "id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"]
        }
        return jsonify({"message": "Login successful", "user": user_data}), 200
      

if __name__ == '__main__':
     app.run(debug=True)