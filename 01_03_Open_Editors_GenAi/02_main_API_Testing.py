from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def test():
    return {"Message":"My name is mangesh"}

students = {1:"Mangesh",2:"HImanshu",3:"Rakesh"}

@app.get("/Mangesh/Sambare/app/api")
def student():
    return students



@app.get("/student/{student_id}")
def student_details(student_id:int):
    return {"id":student_id,"name":students[student_id]}


@app.get("/add_student")
def add_student(student_id:int,name:str):
    students[student_id] = name
    return students

### use for post

@app.post("/add_student_diff")
def add_student_diff():
    students["student_id"]="new_name"
    return students


from pydantic import BaseModel
class new_data(BaseModel):
    student_id : int
    name : str

@app.post("/add_student_new_value")
def add_student_new_values(newdata:new_data):
    students[newdata.student_id] = newdata.name
    return students