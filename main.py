from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from utils import calcular_atributos_partido, graficar_radar_rango_promedio_minimalista

import io

app = FastAPI(
    title="⚽ Radar Chart API",
    description="Visualización táctica de rendimiento futbolístico",
    version="1.0.0",
    docs_url="/api",
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.api_route("/ping", methods=["GET", "HEAD"])
def ping():
    return {"status": "ok"}

@app.post("/graficar")
async def graficar(request: Request):
    datos = await request.json()
    team_a = datos.get("team_a_name")
    team_b = datos.get("team_b_name")
    teams_data = datos.get("teams_data")

    if not team_a or not team_b or not teams_data:
        return JSONResponse(content={"error": "Faltan campos requeridos"}, status_code=400)

    return graficar_radar_rango_promedio_minimalista(team_a, team_b, teams_data)

@app.get("/", response_class=HTMLResponse)
def landing_page():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>⚽ Radar Chart API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: url('https://images.unsplash.com/photo-1587394521422-2cce6d0d5f12?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80') no-repeat center center fixed;
                background-size: cover;
                color: white;
                text-align: center;
                padding: 5%;
                backdrop-filter: brightness(0.6);
            }
            h1 {
                font-size: 3rem;
                margin-bottom: 1rem;
            }
            p {
                font-size: 1.2rem;
            }
            a {
                color: #ffdb4d;
                text-decoration: none;
                font-weight: bold;
            }
            .container {
                background: rgba(0, 0, 0, 0.6);
                padding: 2rem;
                border-radius: 20px;
                max-width: 600px;
                margin: auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏟️ Radar Chart API</h1>
            <p>📊 Visualización táctica de rendimiento futbolístico</p>
            <p>🔧 Desarrollado con <strong>FastAPI + Python + Matplotlib</strong></p>
            <p>⚙️ Endpoint: <code>POST /graficar</code></p>
            <p>🔗 <a href="https://github.com/tuusuario/radar-api" target="_blank">Ver en GitHub</a></p>
        </div>
    </body>
    </html>
    """
