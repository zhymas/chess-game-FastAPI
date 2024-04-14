from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
import uvicorn
from models import Game
from db import create_table, get_result, save_match_result

app=FastAPI()
game=None

@app.post("/start_game")
async def start_game(player1: str, player2: str):
    global game
    game = Game(player1, player2)
    game.start_game()
    create_table()
    return {"message": "Start", "player1": player1, "player2": player2}


@app.post("/move")
async def move(player: str, from_positions: str, to_positions: str):
    if game is None:
        raise HTTPException(status_code=400, detail="Гра не розпочата")
    
    from_positions = tuple(map(int, from_positions.split(',')))
    to_positions = tuple(map(int, to_positions.split(',')))

    if game.move(player, from_positions, to_positions):
        return {"success": True, "message": "move passed"}
    else:
        raise HTTPException(status_code=400, detail="incorrect move")


@app.get("/get_records")
async def get_match_results():
    result = get_result()
    return JSONResponse(content={"success": True, "data": result})

@app.get("/get_board")
def get_board():
    if game == None:
        return {"success": False, "msg": "game not started"}
    return game.get_board()


@app.post("/finish_early", response_class=HTMLResponse)
async def finish_early(winner_name: str):
    if game is None:
        raise HTTPException(status_code=400, detail="Гра не розпочата")
    game.end_game(winner_name)
    return JSONResponse(content={"success": True, "winner": winner_name})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)