from fastapi import FastAPI
import random
from datetime import datetime
import asyncio  # Added missing import
from fastapi import WebSocket, WebSocketDisconnect

app = FastAPI()

# Initial state for 8 tanks with midpoint values from ideal ranges
kpi_state = {
    f"tank{i+1}": {
        "ammonia_mgL": 0.25,
        "nitrite_mgL": 0.25,
        "nitrate_ppm": 10.0,
        "water_level_m": 3.0,
        "pH": 7.0,
        "salinity_ppt": 1.0,
        "suspended_solids_mgL": 5.0,
        "temperature_C": 25.0,
        "dissolved_oxygen_mgL": 6.5,
        "bacteria_health": 0.9,
        "timestamp": datetime.utcnow().isoformat()
    } for i in range(8)
}

# Monitoring flag
monitoring_enabled = True

def update_kpi_value(current_value, min_value, max_value, delta_range):
    delta = random.uniform(-delta_range, delta_range)
    new_value = current_value + delta
    return max(min_value, min(max_value, new_value))

async def generate_kpi_data():
    global kpi_state
    if not monitoring_enabled:
        return kpi_state  # Return last known state without updating
    for tank_id in kpi_state:
        kpi_state[tank_id]["ammonia_mgL"] = update_kpi_value(kpi_state[tank_id]["ammonia_mgL"], 0, 0.5, 0.1)
        kpi_state[tank_id]["nitrite_mgL"] = update_kpi_value(kpi_state[tank_id]["nitrite_mgL"], 0, 0.5, 0.1)
        kpi_state[tank_id]["nitrate_ppm"] = update_kpi_value(kpi_state[tank_id]["nitrate_ppm"], 0, 20, 1.0)
        kpi_state[tank_id]["water_level_m"] = update_kpi_value(kpi_state[tank_id]["water_level_m"], 1, 5, 0.2)
        kpi_state[tank_id]["pH"] = update_kpi_value(kpi_state[tank_id]["pH"], 6.5, 7.5, 0.2)
        kpi_state[tank_id]["salinity_ppt"] = update_kpi_value(kpi_state[tank_id]["salinity_ppt"], 0, 2, 0.1)
        kpi_state[tank_id]["suspended_solids_mgL"] = update_kpi_value(kpi_state[tank_id]["suspended_solids_mgL"], 0, 10, 0.5)
        kpi_state[tank_id]["temperature_C"] = update_kpi_value(kpi_state[tank_id]["temperature_C"], 23, 27, 0.3)
        kpi_state[tank_id]["dissolved_oxygen_mgL"] = update_kpi_value(kpi_state[tank_id]["dissolved_oxygen_mgL"], 5, 8, 0.2)
        kpi_state[tank_id]["bacteria_health"] = update_kpi_value(kpi_state[tank_id]["bacteria_health"], 0.8, 1.0, 0.05)
        kpi_state[tank_id]["timestamp"] = datetime.utcnow().isoformat()
    return kpi_state

@app.post("/webhook")
async def webhook(reset: bool = False):
    kpi_data = await generate_kpi_data()
    return kpi_data

@app.post("/start-monitoring")
async def start_monitoring():
    global monitoring_enabled
    monitoring_enabled = True
    return {"message": "Monitoring started"}

@app.post("/stop-monitoring")
async def stop_monitoring():
    global monitoring_enabled
    monitoring_enabled = False
    return {"message": "Monitoring stopped"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            if monitoring_enabled:
                data = await generate_kpi_data()
                await websocket.send_json(data)
            await asyncio.sleep(5)  # Send updates every 5 seconds
    except WebSocketDisconnect:
        pass