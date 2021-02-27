from flask import Flask, jsonify, render_template
from flask_restful import reqparse
import re
from openpyxl import load_workbook
import urllib
import json

app = Flask(__name__)
if __name__ == '__main__':
    app.run(threaded=True)

parser = reqparse.RequestParser()
parser.add_argument('day', type=str, required=False)
parser.add_argument('program', type=str, required=False)
parser.add_argument('section', type=str, required=False)
parser.add_argument('course', type=str, required=False)
parser.add_argument('slot', type=int, required=False)
parser.add_argument('teacher', type=str, required=False)


def time_setter(t):
    if(t==1):
        return "8:00-9:00"
    elif(t==2):
        return "9:00-10:00"
    elif(t==3):
        return "10:00-11:00"
    elif(t==4):
        return "11:00-12:00"
    elif(t==5):
        return "12:00-1:00"
    elif(t==6):
        return "1:00-2:00"
    elif(t==7):
        return "2:00-3:00"
    elif(t==8):
        return "3:00-4:00"
    elif(t==9):
        return "4:00-5:00"
    

@app.route('/details/<string:course>')
def details(course):
    course = urllib.parse.unquote_plus(course)
    l = []
    with open("data.txt", "r") as f:
        l = json.load(f)

    r = []
    for x in l:
        if x["Course Name"] == course:
            r.append(x)
    return jsonify(r)
@app.route('/search')
def search():
    program = str(parser.parse_args().get('program', None)).upper()
    section = str(parser.parse_args().get('section', None)).upper()
    day = str(parser.parse_args().get('day', None)).upper()
    teacher = str(parser.parse_args().get('teacher', None)).upper()
    slot = parser.parse_args().get('slot', None)
    course = str(parser.parse_args().get('course', None)).upper()
    
    s=[]
    if program!="NONE":
        s.append(program)
    if course!="NONE":
        s.append(course)
    if teacher!="NONE":
        s.append(teacher)
    if section!="NONE":
        s.append(section)

    l = []
    with open("data.txt", "r") as f:
        l = json.load(f)

    r = []
    for x in l:
        print(s)
        print(day)
        print(slot)
        if day!="NONE" and x["Day"]!=day:
            continue
        if slot is not None and x["Slot"]!=slot:
            continue
        if all(y in x["Course Name"] for y in s):
            r.append(x)
        
    return jsonify(r)

@app.route('/names')
def names():
    with open("data.txt", "r") as f:
        l = json.load(f)
        
    r = []
    for x in l:
        if x["Course Name"] not in r:
            r.append(x["Course Name"])
    return jsonify(r)

@app.route('/navigate')
def nav():
    with open("data.txt", "r") as f:
        l = json.load(f)
    course_names = [[]]

    for x in l:
        if x["Course Name"] not in course_names:
            course_names.append([x["Course Name"], "details/" + urllib.parse.quote_plus(x["Course Name"])])
    
    return render_template("index.html", course_names=course_names)