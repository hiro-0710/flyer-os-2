from fastapi import WebSocket, WebSocketDisconnect

from modules.intent_engine import parse_intent
from modules.decision_engine import decide_action
from modules.action_executor import execute_action
from utils.logger import log_info, log_error


async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    log_info("WebSocket connected")

    try:
        while True:
            data = await websocket.receive_json()

            text = data.get("content", "") or ""
            log_info(f"Received from UI: {text}")

            intent = parse_intent(text)
            decision = decide_action(intent)
            result = execute_action(decision)

            await websocket.send_json(
                {
                    "type": "action",
                    "content": result,
                    "meta": {
                        "intent": intent,
                        "decision": decision,
                    },
                }
            )

    except WebSocketDisconnect:
        log_info("WebSocket disconnected")
    except Exception as e:
        log_error(f"WebSocket error: {e}")
        await websocket.close()
