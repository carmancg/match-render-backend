from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import matplotlib.pyplot as plt
import numpy as np
import io
from fastapi.responses import StreamingResponse

app = FastAPI()

# Habilita CORS para que el frontend pueda hacer peticiones sin problema
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # puedes restringir esto a tu frontend si gustas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta básica de prueba
@app.get("/")
def root():
    return {"mensaje": "API Radar Chart está viva"}

# Ruta especial para UptimeRobot
@app.api_route("/ping", methods=["GET", "HEAD"])
def ping():
    return {"status": "ok"}
