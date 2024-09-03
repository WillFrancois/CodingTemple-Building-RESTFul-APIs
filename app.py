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
        req = request.get_json()
        member_schema = Members.MemberUpdateSchema()
        member = Members.MemberUpdateSchema.load(member_schema, data=req)

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


#Task 3 (Session CRUD starts here!)
#NOTE: Assignment did not specify creation of deletion function like the previous task, so one was not made
@app.route("/sessions", methods=["POST"])
def create_session():
    try:
        req = request.get_json()
        print(req)
        workout_schema = WorkoutSessions.WorkoutSchema()
        session = WorkoutSessions.WorkoutSchema.load(workout_schema, data=req)

        cur = conn.cursor()
        cur.execute("insert into WorkoutSessions(session_id, member_id, session_date, session_time, activity) values(%s, %s, %s, %s, %s)", [session["s_id"], session["m_id"], session["s_date"], session["s_time"], session["activity"]])
        conn.commit()
        cur.close()
        return "Success, session added."

    except Exception as e:
        return f"Could not complete request. {e}"

@app.route("/sessions/<int:id>", methods=['GET'])
def view_session(id):
    try:
        cur = conn.cursor()
        cur.execute("select * from WorkoutSessions where session_id = %s", [id])
        data = cur.fetchone()
        cur.close()
        return jsonify({'session_id': data[0], 'member_id': data[1], 'session_date': data[2], 'session_time': data[3], 'activity': data[4]})
    except Exception as e:
        return f"Could not find session. Incorrect ID provided or database is unavailable."


@app.route("/sessions/<int:id>", methods=["PUT"])
def update_session(id):
    try:
        req = request.get_json()
        workout_schema = WorkoutSessions.WorkoutUpdateSchema()
        session = WorkoutSessions.WorkoutUpdateSchema.load(workout_schema, data=req)

        cur = conn.cursor()
        cur.execute("update WorkoutSessions set session_date = %s, session_time = %s, activity = %s where session_id = %s", [session["s_date"], session["s_time"], session["activity"], id])
        conn.commit()
        cur.close()
        return "Success, session updated."

    except Exception as e:
        return f"Could not complete request. {e}"

@app.route("/sessions/member/<int:m_id>", methods=["GET"])
def users_sessions(m_id):
    try:
        cur = conn.cursor()
        cur.execute("select * from WorkoutSessions inner join Members where Members.id=WorkoutSessions.member_id and member_id = %s", [m_id])
        data = cur.fetchall()
        cur.close()

        return_value = {}
        for point in range(0, len(data)):
            return_value[point] = {"Session_ID": data[point][0], "Member_ID": data[point][1], "Session_Date": data[point][2], "Session_Time": data[point][3], "Activity": data[point][4], "Member_Name": data[point][6]}
        return jsonify(return_value)

    except Exception as e:
        return f"Could not complete request. {e}"
