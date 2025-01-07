from fastapi import FastAPI
from functions import (
    cantidad_filmaciones_mes,
    cantidad_filmaciones_dia,
    score_titulo,
    votos_titulo,
    get_actor,
    get_director,
)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de películas"}

@app.get("/cantidad_filmaciones_mes/")
def api_cantidad_filmaciones_mes(mes: str):
    return {"result": cantidad_filmaciones_mes(mes)}

@app.get("/cantidad_filmaciones_dia/")
def api_cantidad_filmaciones_dia(dia: str):
    return {"result": cantidad_filmaciones_dia(dia)}

@app.get("/score_titulo/")
def api_score_titulo(titulo: str):
    return {"result": score_titulo(titulo)}

@app.get("/votos_titulo/")
def api_votos_titulo(titulo: str):
    return {"result": votos_titulo(titulo)}

@app.get("/actor/")
def api_actor(nombre_actor: str):
    return {"result": get_actor(nombre_actor)}

@app.get("/director/")
def api_director(nombre_director: str):
    return {"result": get_director(nombre_director)}

