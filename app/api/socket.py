from fastapi import APIRouter, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.repositories import SensorRepository
import httpx, asyncio, json

router = APIRouter()
clients = []
API_URL = "https://moriahmkt.com/iotapp/test/"
INTERVALO = 5


@router.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except:
        clients.remove(websocket)


async def poll_and_broadcast(db: AsyncSession):
    repo = SensorRepository(db)
    last_data = None
    while True:
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(API_URL)
                if res.status_code == 200:
                    data = res.json()
                    if data != last_data:
                        await repo.save_sensor_general(data["sensores"])
                        for parcela in data["parcelas"]:
                            await repo.save_parcela_data(parcela)

                        for client in clients:
                            await client.send_text(json.dumps(data))
                        last_data = data
        except Exception as e:
            print("Error polling:", e)
        await asyncio.sleep(INTERVALO)
