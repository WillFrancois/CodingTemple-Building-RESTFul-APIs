#Task 1
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow

import mysql.connector
import Members
import WorkoutSessions

app = Flask(__name__)
ma = Marshmallow(app)

try:
    conn = mysql.connector.connect(user='root', password='my-secret-pw', host='localhost', database='FitnessCenter') #Default credentials for the MySQL docker container
except Exception as e:
    print(f"Could not connect to database: {e}")

@app.route("/", methods=['GET'])
def home():
    return ("Welcome to the FitnessCenter API!<br>Use the /members route for members related calls.<br>Use the /sessions route for Workout Session calls.")

#Task 2 (Member CRUD starts here!)
@app.route("/members", methods=['POST'])
def add_member():
    try:
        #Receive and validate member information
        req = request.get_json()
        member_schema = Members.MemberSchema()
        member = Members.MemberSchema.load(member_schema, data=req)

        #Append to database
        cur = conn.cursor()
        cur.execute("insert into Members(id, name, age) values(%s, %s, %s)", [member["pk"], member["name"], member["age"]])
        conn.commit()
        cur.close()
        return "Success, user added."

    except Exception as e:
        return f"Could not complete request. {e}"

@app.route("/members/<int:id>", methods=['GET'])
def view_member(id):
    try:
        cur = conn.cursor()
        cur.execute("select * from Members where id = %s", [id])
        data = cur.fetchone()
        cur.close()
        return jsonify({'id': data[0], 'name': data[1], 'age': data[2]})
    except Exception as e:
        return f"Could not find user. Incorrect ID provided or database is unavailable."

@app.route("/members/<int:id>", methods=["PUT"])
def update_member(id):
    try:
        #Receive and validate member information
        req = request.get_json()
        member_schema = Members.MemberUpdateSchema()
        member = Members.MemberUpdateSchema.load(member_schema, data=req)

        #Append to database
        cur = conn.cursor()
        cur.execute("update Members set name = %s, age = %s where id = %s", [member["name"], member["age"], id])
        conn.commit()
        cur.close()
        return "Success, user updated."

    except Exception as e:
        return f"Could not complete request. {e}"

@app.route("/members/<int:id>", methods=["DELETE"])
def remove_member(id):
    try:
        cur = conn.cursor()
        cur.execute("delete from Members where id = %s", [id])
        conn.commit()
        cur.close()
        return "Deletion successful!"
    except Exception as e:
        return f"Could not find user. Incorrect ID provided or database is unavailable."
