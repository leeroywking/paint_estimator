from flask import Flask
from flask_cors 

app = Flask(__name__)

@app.get("/")
def hello():
    return {"ok": True}

# @app.post("/flatten_image")
