from fastapi import FastAPI
import os
#from dotenv import load_dotenv

#load_dotenv()
app = FastAPI()

@app.get("/")
def hello():
    print(os.environ['Env'])
    return {
        "message":"Hello world",
        "stupidenv":os.environ['Env']
        }