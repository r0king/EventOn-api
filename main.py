
import os
from fastapi.params import Body
from typing import Optional
from fastapi import FastAPI,Request
from plugins.sheetAccess.sheets import NewSheet
app = FastAPI()


@app.get("/")
def read_root(user_id:str,request: Request):

    client_host = request.client.host

    newspreadsheet = NewSheet(user_id=user_id,sheet_name='Student List')

    return newspreadsheet


@app.get("/items/{item_id}")
def read_item(item_id: int, request: Request):
    return {"item_id": item_id, "q": q}