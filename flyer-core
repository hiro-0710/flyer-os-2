from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Flyer Core Minimal")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- Intent Engine --------
def parse_intent(text: str) -> str:
    t = (text or "").lower()

    if "次" in text or "進" in text:
        return "next_step"
    if "戻" in text or "前" in text:
        return "previous_step"
    if "状態" in text or "ステータス" in text:
        return "status_check"
    if any(g in text for g in ["こんにちは", "やあ", "おはよう", "こんばんは"]):
        return "greeting"

    return "unknown"


# -------- Decision Engine --------
def decide_action(intent: str):
    if intent == "next_step":
        return {"type": "navigation", "action": "go_next"}
    if intent == "previous_step":
        return {"type": "navigation", "action": "go_previous"}
    if intent == "status_check":
        return {"type": "status", "action": "report"}
    if intent == "greeting":
        return {"type": "greeting", "action": "respond"}

    return {"type": "unknown", "action": "none"}


# -------- Action Executor --------
def execute_action(decision: dict) -> str:
    dtype = decision["type"]
    action = decision["action"]

    if dtype == "navigation" and action == "go_next":
        return "次のフェーズに静かに移行します。"
    if dtype == "navigation" and action == "go_previous":
        return "ひとつ前のフェーズに戻ります。"
    if dtype == "status" and action == "report":
        return "現在は development フェーズ。Flyer Core は正常に稼働しています。"
    if dtype == "greeting" and action == "respond":
        return "こんにちは、Flyerです。必要なときだけ静かに最適化します。"

    return "意図をまだうまくつかめていません。"


# -------- WebSocket --------
@app.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()
            text = data.get("content", "")

            intent = parse_intent(text)
            decision = decide_action(intent)
            result = execute_action(decision)

            await websocket.send_json({
                "type": "action",
                "content": result,
                "meta": {
                    "intent": intent,
                    "decision": decision
                }
            })

    except WebSocketDisconnect:
        pass


@app.get("/")
def root():
    return {"status": "Flyer Core running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
