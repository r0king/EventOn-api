from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def hello():
    print(os.environ['Env'])
    return {
        "message":"Hello world",
        "stupid-env":os.environ['Env']
        }