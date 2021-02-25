from flask import Flask, jsonify, render_template
import re
from openpyxl import load_workbook
import urllib

app = Flask(__name__)

@app.route('/details/<string:course>')
def details(course):
    course = urllib.parse.unquote_plus(course)
    wb = load_workbook(filename='timetable.xlsx')
    l = []
    for sheet in wb.worksheets:
        if sheet.title=="Monday" or sheet.title=="Tuesday" or sheet.title=="Wednesday" or sheet.title=="Thursday" or sheet.title=="Friday" or sheet.title=="Saturday" or sheet.title=="Sunday":
            for i in range(1, sheet.max_row + 1):
                for j in range(sheet.max_column):
                    if (str(sheet[i][j].value).find("BCS") != -1 or str(sheet[i][j].value).find("BDS") != -1 or str(sheet[i][j].value).find("BAI") != -1 or str(sheet[i][j].value).find("BSE") != -1):
                        l.append({"Course Name": (" ".join(sheet[i][j].value.split()).upper().replace("/", "&")), "Day": (sheet.title.upper()), "Venue: ": (sheet[i][0].value.upper()), "Slot": (sheet[2][j].value)})
                        if str(sheet[i][j].value).find("Lab") != -1 or str(sheet[i][j].value).find("lab") != -1:
                            l.append({"Course Name": (" ".join(sheet[i][j].value.split()).upper().replace("/", "&")), "Day": (sheet.title.upper()), "Venue: ": (sheet[i][0].value.upper()), "Slot": (sheet[2][j].value)+1})
                            l.append({"Course Name": (" ".join(sheet[i][j].value.split()).upper().replace("/", "&")), "Day": (sheet.title.upper()), "Venue: ": (sheet[i][0].value.upper()), "Slot": (sheet[2][j].value)+2})

    
    r = []
    for x in l:
        if x["Course Name"] == course:
            r.append(x)
    return jsonify(r)


@app.route('/names')
def names():
    wb = load_workbook(filename='timetable.xlsx')
    l = []
    for sheet in wb.worksheets:
        if sheet.title=="Monday" or sheet.title=="Tuesday" or sheet.title=="Wednesday" or sheet.title=="Thursday" or sheet.title=="Friday" or sheet.title=="Saturday" or sheet.title=="Sunday":
            for i in range(1, sheet.max_row + 1):
                for j in range(sheet.max_column):
                    if str(sheet[i][j].value).find("BCS") != -1 or str(sheet[i][j].value).find("BDS") != -1 or str(sheet[i][j].value).find("BAI") != -1 or str(sheet[i][j].value).find("BSE") != -1:
                        l.append({"Course Name": (" ".join(sheet[i][j].value.split()).upper().replace("/", "&")), "Day": (sheet.title.upper()), "Venue: ": (sheet[i][0].value.upper()), "Slot": (sheet[2][j].value)})
                        if str(sheet[i][j].value).find("Lab") != -1 or str(sheet[i][j].value).find("lab") != -1:
                            l.append({"Course Name": (" ".join(sheet[i][j].value.split()).upper().replace("/", "&")), "Day": (sheet.title.upper()), "Venue: ": (sheet[i][0].value.upper()), "Slot": (sheet[2][j].value)+1})
                            l.append({"Course Name": (" ".join(sheet[i][j].value.split()).upper().replace("/", "&")), "Day": (sheet.title.upper()), "Venue: ": (sheet[i][0].value.upper()), "Slot": (sheet[2][j].value)+2})
    
    r = []
    for x in l:
        if x["Course Name"] not in r:
            r.append(x["Course Name"])
    return jsonify(r)

@app.route('/navigate')
def nav():
    wb = load_workbook(filename='timetable.xlsx')
    l = []
    dupli=[]
    for sheet in wb.worksheets:
        if sheet.title=="Monday" or sheet.title=="Tuesday" or sheet.title=="Wednesday" or sheet.title=="Thursday" or sheet.title=="Friday" or sheet.title=="Saturday" or sheet.title=="Sunday":
            for i in range(1, sheet.max_row + 1):
                for j in range(sheet.max_column):
                    if (str(sheet[i][j].value).find("BCS") != -1 or str(sheet[i][j].value).find("BDS") != -1 or str(sheet[i][j].value).find("BAI") != -1 or str(sheet[i][j].value).find("BSE") != -1) and (" ".join(sheet[i][j].value.split()).upper().replace("/", "&")) not in dupli:
                        l.append({"Course Name": (" ".join(sheet[i][j].value.split()).upper().replace("/", "&")), "Day": (sheet.title.upper()), "Venue: ": (sheet[i][0].value.upper()), "Slot": (sheet[2][j].value)})

    course_names = [[]]

    for x in l:
        if x["Course Name"] not in course_names:
            course_names.append([x["Course Name"], "details/" + urllib.parse.quote_plus(x["Course Name"])])
    
    return render_template("index.html", course_names=course_names)


