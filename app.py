from flask import Flask, render_template, request, redirect
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import os
import time

app = Flask(__name__)

# Read CSV Data
def get_data():
    return pd.read_csv("students.csv")


# Generate Graphs
def create_graphs():

    df = get_data()

    subjects = ["Math", "Science", "English"]

    if df.empty:
        return

    # Graph 1: Student Total Marks
    total_marks = df[subjects].sum(axis=1)

    plt.figure(figsize=(8, 5))
    plt.bar(df["Name"], total_marks)
    plt.title("Student Total Marks")
    plt.xlabel("Students")
    plt.ylabel("Total Marks")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("static/bar_chart.png")
    plt.close()

    # Graph 2: Subject Performance Pie Chart
    subject_avg = df[subjects].mean()

    plt.figure(figsize=(7, 5))
    plt.pie(
        subject_avg,
        labels=subjects,
        autopct='%1.1f%%',
        startangle=90
    )
    plt.title("Subject Performance")
    plt.savefig("static/pie_chart.png")
    plt.close()

    # Graph 3: Subject Comparison
    plt.figure(figsize=(8, 5))
    plt.bar(subjects, subject_avg)
    plt.title("Average Marks by Subject")
    plt.xlabel("Subjects")
    plt.ylabel("Average Marks")
    plt.tight_layout()
    plt.savefig("static/subject_chart.png")
    plt.close()


# Home Page
@app.route("/")
def home():

    df = get_data()

    subjects = ["Math", "Science", "English"]

    marks = df[subjects].values

    average = round(np.mean(marks), 2)
    highest = marks.max()
    lowest = marks.min()

    create_graphs()

    return render_template(
        "index.html",
        tables=df.to_html(index=False),
        average=average,
        highest=highest,
        lowest=lowest,
        total_students=len(df),
        graph_version=int(time.time())
    )


# Add Student
@app.route("/add", methods=["POST"])
def add_student():

    name = request.form["name"].strip()

    math = int(request.form["math"])
    science = int(request.form["science"])
    english = int(request.form["english"])

    if not name or any(
        mark < 0 or mark > 100
        for mark in [math, science, english]
    ):
        return "Invalid student details or marks!"

    df = get_data()

    new_student = pd.DataFrame([{
        "Name": name,
        "Math": math,
        "Science": science,
        "English": english
    }])

    df = pd.concat([df, new_student], ignore_index=True)

    df.to_csv("students.csv", index=False)

    return redirect("/")


if __name__ == "__main__":

    os.makedirs("static", exist_ok=True)

    app.run(debug=True)