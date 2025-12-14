from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor


app = FastAPI()

db_url = 'postgresql://neondb_owner:npg_TQ0CLxylo5zB@ep-nameless-bonus-a85rq9uh-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require'

class students(BaseModel):
    id : int
    name : str
    age : int


def get_connection_url():
    conn = psycopg2.connect(db_url,cursor_factory=RealDictCursor)
    return conn


def save_student_to_file(data):
    with open ("student.txt","a") as f:
        f.write(f"{data.id},{data.name},{data.age}\n")
        
@app.post("/students")
def create_student(stud:students):
    save_student_to_file(stud)
    return {"message":"Student data saved successfully"}
    

@app.post("/students/db/insert")
def store_student_in_db(student: students):
    conn = get_connection_url()
    cursor = conn.cursor()
    insert_query = "INSERT INTO STUDENT (id, name, age) VALUES  (%s,%s,%s)"
    cursor.execute(insert_query,(student.id, student.name,student.age))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message":"student data inserted into database successfully"}

@app.post("/students/db/update")
def update_student_in_db(student: students):
    conn = get_connection_url()
    cursor = conn.cursor()

    update_query = "UPDATE student SET age = %s WHERE id = %s"

    cursor.execute(update_query, (student.age, student.id))

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Student data updated successfully"}