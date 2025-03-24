from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.models import SensorNodoGeneral, Parcela, SensorParcelaHistorico
from datetime import datetime

class SensorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_sensor_general(self, data):
        sensor = SensorNodoGeneral(**data)
        self.db.add(sensor)
        await self.db.commit()

    async def save_parcela_data(self, parcela_data):
        # Verifica si la parcela ya existe
        stmt = select(Parcela).where(Parcela.parcela_id == parcela_data["id"])
        result = await self.db.execute(stmt)
        parcela_existente = result.scalar_one_or_none()

        # Si no existe, insertamos la parcela
        if not parcela_existente:
            nueva_parcela = Parcela(
                parcela_id=parcela_data["id"],
                nombre=parcela_data["nombre"],
                ubicacion=parcela_data["ubicacion"],
                responsable=parcela_data["responsable"],
                tipo_cultivo=parcela_data["tipo_cultivo"],
                latitud=parcela_data["latitud"],
                longitud=parcela_data["longitud"]
            )
            self.db.add(nueva_parcela)
            await self.db.commit()

        # Convertir 'ultimo_riego' de string a datetime
        try:
            ultimo_riego_str = parcela_data["ultimo_riego"]
            ultimo_riego_dt = datetime.strptime(ultimo_riego_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            ultimo_riego_dt = datetime.fromisoformat(ultimo_riego_str)

        # Insertar lectura histórica del sensor de la parcela
        sensor = parcela_data["sensor"]

        historico = SensorParcelaHistorico(
            parcela_id=parcela_data["id"],
            humedad=sensor["humedad"],
            temperatura=sensor["temperatura"],
            lluvia=int(sensor["lluvia"]),
            sol=int(sensor["sol"]),
            ultimo_riego=ultimo_riego_dt
        )

        try:
            self.db.add(historico)
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            print("❌ Error guardando histórico:", e)