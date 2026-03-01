from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample Database (Dictionary)
students = {}

# Home Dashboard
@app.route("/")
def dashboard():

    q = request.args.get("q")

    if q:
        q = q.lower()
        filtered = {}

        for roll, data in students.items():
            if q in data["name"].lower():
                filtered[roll] = data

        return render_template("dashboard.html", students=filtered)

    return render_template("dashboard.html", students=students)


# Add Student
@app.route("/add", methods=["POST"])
def add_student():

    roll = request.form.get("roll")
    name = request.form.get("name")

    # Marks
    hci = int(request.form.get("hci") or 0)
    isecurity = int(request.form.get("isecurity") or 0)
    mad = int(request.form.get("mad") or 0)
    daa = int(request.form.get("daa") or 0)
    bda = int(request.form.get("bda") or 0)

    total = hci + isecurity + mad + daa + bda
    avg = total / 5

    # CGPA Calculation (Simple Formula)
    cgpa = round((avg / 100) * 4, 2)

    # Grade
    if avg >= 80:
        grade = "A"
    elif avg >= 70:
        grade = "B"
    elif avg >= 60:
        grade = "C"
    else:
        grade = "F"

    students[roll] = {
        "name": name,
        "total": total,
        "average": avg,
        "cgpa": cgpa,
        "grade": grade
    }

    return redirect(url_for("dashboard"))


# Delete Student
@app.route("/delete/<roll>")
def delete_student(roll):
    students.pop(roll, None)
    return redirect(url_for("dashboard"))


# Search Student
@app.route("/search")
def search_student():

    roll = request.args.get("q")

    student = students.get(roll)

    return render_template(
        "search_result.html",
        student=student,
        roll=roll
    )

if __name__ == "__main__":
    app.run(debug=True)