"""
tools.py
Simple tool functions that the agent can call.
These are local mock tools (no external APIs) so everything runs offline.
"""
from typing import Dict, Any

def turn_on_light(room: str) -> Dict[str, Any]:
    return {"status": "ok", "action": "turn_on_light", "room": room, "message": f"Light turned on in {room}."}

def set_temperature(temp: int) -> Dict[str, Any]:
    return {"status": "ok", "action": "set_temperature", "temp": temp, "message": f"Temperature set to {temp}°C."}

def get_schedule(date: str) -> Dict[str, Any]:
    # simple mock schedule
    schedules = {
        "2025-12-01": ["09:00 Meeting with team", "13:00 Lunch with mentor"],
        "2025-12-02": ["10:00 Doctor", "15:00 Project review"]
    }
    return {"status": "ok", "date": date, "events": schedules.get(date, [])}

def help_text() -> str:
    return (
        "I understand commands like:\n"
        "- 'turn on the kitchen light'\n"
        "- 'set temperature to 24'\n"
        "- 'what's my schedule on 2025-12-01'\n"
        "- 'remember my favorite drink is coffee'\n"
        "- 'what did I ask you to remember?'\n        "
    )

