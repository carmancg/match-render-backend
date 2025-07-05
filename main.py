from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import matplotlib.pyplot as plt
import uuid
from utils import graficar_radar_rango_promedio_minimalista

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
    teams_data = data["teams_data"]  # formato tipo manu_ast

    filename = f"{uuid.uuid4()}.png"
    graficar_radar_rango_promedio_minimalista(team_a_name, team_b_name, teams_data)
    plt.savefig(filename, bbox_inches="tight")
    return FileResponse(filename, media_type="image/png", filename="radar.png")

@app.get("/")
def home():
    return {"mensaje": "Radar Chart activo"}
