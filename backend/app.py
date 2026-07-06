from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import time

app = Flask(__name__)
CORS(app)

# Wait until MySQL is ready
db = None

while True:
    try:
        db = pymysql.connect(
            host="mysql",
            user="root",
            password="root123",
            database="studentdb",
            cursorclass=pymysql.cursors.DictCursor
        )
        print("✅ Connected to MySQL!")
        break
    except Exception as e:
        print(f"⏳ Waiting for MySQL... {e}")
        time.sleep(5)


@app.route("/students", methods=["GET"])
def get_students():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    return jsonify(rows)


@app.route("/students", methods=["POST"])
def add_student():
    data = request.json

    cursor = db.cursor()

    sql = """
    INSERT INTO students(name, email, course)
    VALUES(%s, %s, %s)
    """

    cursor.execute(sql, (
        data["name"],
        data["email"],
        data["course"]
    ))

    db.commit()

    return jsonify({"message": "Student Added Successfully"})


@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=%s",
        (id,)
    )

    db.commit()

    return jsonify({"message": "Student Deleted Successfully"})


@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.json

    cursor = db.cursor()

    sql = """
    UPDATE students
    SET name=%s,
        email=%s,
        course=%s
    WHERE id=%s
    """

    cursor.execute(sql, (
        data["name"],
        data["email"],
        data["course"],
        id
    ))

    db.commit()

    return jsonify({"message": "Student Updated Successfully"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
