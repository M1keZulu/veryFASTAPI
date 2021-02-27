from fastapi import FastAPI, Form, Request
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import json
from typing import Optional
import urllib

#Deploy

app=FastAPI()
templates = Jinja2Templates(directory="templates/")

@app.get('/details/{course}')
async def alpha(course: str):
    with open("data.txt", "r") as f:
        l = json.load(f)
    
    r=[]
    for x in l:
        if x["Course Name"] == course.upper():
            r.append(x)
    return r

@app.get('/names')
def names():
    with open("data.txt", "r") as f:
        l = json.load(f)
        
    r = []
    for x in l:
        if x["Course Name"] not in r:
            r.append(x["Course Name"])
    return r

@app.get('/navigate', response_class=HTMLResponse)
async def nav(request: Request):
    with open("data.txt", "r") as f:
        l = json.load(f)
    
    course_names = [[]]
    for x in l:
        if x["Course Name"] not in course_names:
            course_names.append([x["Course Name"], "details/" + x["Course Name"]])
    
    return templates.TemplateResponse("index.html", {"request": request, "course_names": course_names})

@app.get('/search')
async def search(course: Optional[str]=None, section: Optional[str]=None, day: Optional[str]=None, teacher: Optional[str]=None, program: Optional[str]=None, slot: Optional[int]=None):
    with open("data.txt", "r") as f:
        l = json.load(f)
    r = []
    s=[]
    if course is not None:
        s.append(course.upper())
    if section is not None:
        s.append(section.upper())
    if program is not None:
        s.append(program.upper())
    if teacher is not None:
        s.append(teacher.upper())

    for x in l:
        if day is not None and x["Day"]!=day.upper():
            continue
        if slot is not None and x["Slot"]!=slot:
            continue
        if all(y in x["Course Name"] for y in s):
            r.append(x)
    return r
    