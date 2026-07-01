from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

db = pymysql.connect(
    host="mysql",
    user="root",
    password="root123",
    database="studentdb"
)

@app.route("/students", methods=["GET"])
def get_students():

    cursor = db.cursor()

    cursor.execute("SELECT * FROM students")

    rows = cursor.fetchall()

    data=[]

    for row in rows:
        data.append({
            "id":row[0],
            "name":row[1],
            "email":row[2],
            "course":row[3]
        })

    return jsonify(data)

@app.route("/students", methods=["POST"])
def add_student():

    data=request.json

    cursor=db.cursor()

    sql="INSERT INTO students(name,email,course) VALUES(%s,%s,%s)"

    cursor.execute(sql,(data["name"],data["email"],data["course"]))

    db.commit()

    return jsonify({"message":"Student Added"})


@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):

    cursor=db.cursor()

    cursor.execute("DELETE FROM students WHERE id=%s",(id))

    db.commit()

    return jsonify({"message":"Deleted"})


@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):

    data=request.json

    cursor=db.cursor()

    sql="UPDATE students SET name=%s,email=%s,course=%s WHERE id=%s"

    cursor.execute(sql,(data["name"],data["email"],data["course"],id))

    db.commit()

    return jsonify({"message":"Updated"})


app.run(host="0.0.0.0",port=5000)