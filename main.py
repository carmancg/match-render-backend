from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uuid
from utils import graficar_5_radares_datos_crudos

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/graficar")
async def graficar(request: Request):
    data = await request.json()
    team_a_name = data["team_a_name"]
    team_b_name = data["team_b_name"]
    teams_data = data["teams_data"]

    filename = f"{uuid.uuid4()}.png"
    graficar_5_radares_datos_crudos(teams_data, team_a_name, team_b_name, filename)
    return FileResponse(filename, media_type="image/png", filename="radar.png")

@app.get("/")
def home():
    return {"mensaje": "Radar Chart activo"}

@app.api_route("/ping", methods=["GET", "HEAD"])
def ping():
    return {"status": "ok"}
