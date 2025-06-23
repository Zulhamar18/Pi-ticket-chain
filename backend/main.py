from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# CORS: agar frontend bisa akses backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ganti dengan domain frontend jika sudah live
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint untuk verifikasi token Pi
@app.post("/verify-token")
async def verify_token(request: Request):
    body = await request.json()
    access_token = body.get("accessToken")

    if not access_token:
        raise HTTPException(status_code=400, detail="Access token is required")

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    res = requests.get("https://api.minepi.com/v2/me", headers=headers)

    if res.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return res.json()
