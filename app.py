from flask import Flask, render_template, request
import time
import random
from difflib import SequenceMatcher # difflib library using

app = Flask(__name__)

# Sentences for typing test
test = [
    "DevOps is a software development approach that combines development and IT operations to improve collaboration, automate workflows, and deliver applications more efficiently. It focuses on practices such as continuous integration, continuous deployment, version control, infrastructure automation, and monitoring to ensure faster and more reliable software delivery.",
    "Flask is a lightweight Python web framework used to build web applications quickly and efficiently. It provides essential tools for routing, request handling, and template rendering while allowing developers to choose additional libraries as needed. It is widely used for developing dynamic websites.",
    "Git is a distributed version control system that helps developers track changes in source code, manage different versions of a project, and collaborate efficiently. GitHub is a cloud-based platform that hosts Git repositories, enabling developers to store, share, and collaborate on projects while maintaining version history."
]
# Calculate typing errors
def mistake(original, typed):
    similarity = SequenceMatcher(None, original, typed).ratio()
    errors = round((1 - similarity) * len(original))
    return errors

# Calculate typing speed (Words Per Minute)
def speed_time(time_taken, userinput):
    if time_taken <= 0:
        return 0
    words = len(userinput.split())
    wpm = (words * 60) / time_taken
    return round(wpm)

#Routing function applying
@app.route('/')
def home():
    test1 = random.choice(test)
    return render_template("type.html", test1=test1)


@app.route('/result', methods=['POST'])
def result():
    original = request.form["original_text"]
    typed = request.form["input_text"]
    start = float(request.form["start_time"])
    end = time.time()
    total_time = end - start
    speed = speed_time(total_time, typed)
    error = mistake(original, typed)

    return render_template("result.html", speed=speed, time=round(total_time, 2), error=error, typed=typed)

if __name__ == "__main__":
    app.run(debug=True)