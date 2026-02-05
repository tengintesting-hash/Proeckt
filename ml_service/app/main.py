import os
import json
from io import BytesIO
from pathlib import Path
from typing import Any
import numpy as np
import cv2
from fastapi import FastAPI
from pydantic import BaseModel
from PIL import Image
import imagehash
import requests

app = FastAPI(title="ML Service")

DATA_DIR = Path(os.getenv("ML_DATA_DIR", "/data/ml"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
HASH_FILE = DATA_DIR / "media_hashes.json"

BANNED_WORDS = {"porn", "sex", "nude", "xxx", "casino", "bet"}


class ModerateRequest(BaseModel):
    text: str
    media_url: str | None = None
    media_type: str | None = None


class UniquenessRequest(BaseModel):
    media_url: str | None = None
    media_type: str | None = None


class FeedRequest(BaseModel):
    user_id: int
    feed_type: str
    limit: int
    offset: int


def load_hashes() -> list[str]:
    if HASH_FILE.exists():
        return json.loads(HASH_FILE.read_text())
    return []


def save_hashes(hashes: list[str]) -> None:
    HASH_FILE.write_text(json.dumps(hashes))


def fetch_media(media_url: str) -> bytes:
    if media_url.startswith("http"):
        resp = requests.get(media_url, timeout=10)
        resp.raise_for_status()
        return resp.content
    path = Path("/data/media") / Path(media_url).name
    return path.read_bytes()


def text_score(text: str) -> float:
    tokens = {t.lower() for t in text.split()}
    matches = tokens & BANNED_WORDS
    if not tokens:
        return 0.0
    return min(1.0, len(matches) / max(1, len(tokens)))


def skin_ratio(image: np.ndarray) -> float:
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 30, 60], dtype=np.uint8)
    upper = np.array([20, 150, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower, upper)
    ratio = float(np.count_nonzero(mask)) / float(mask.size)
    return ratio


def media_score(media_url: str | None, media_type: str | None) -> float:
    if not media_url or not media_type:
        return 0.0
    data = fetch_media(media_url)
    if media_type.startswith("image"):
        image = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
        return skin_ratio(image)
    if media_type.startswith("video"):
        temp = DATA_DIR / "temp_video"
        temp.write_bytes(data)
        cap = cv2.VideoCapture(str(temp))
        scores = []
        for _ in range(5):
            success, frame = cap.read()
            if not success:
                break
            scores.append(skin_ratio(frame))
        cap.release()
        temp.unlink(missing_ok=True)
        return float(np.mean(scores)) if scores else 0.0
    return 0.0


def compute_hash(media_url: str | None, media_type: str | None) -> str | None:
    if not media_url or not media_type:
        return None
    data = fetch_media(media_url)
    if media_type.startswith("image"):
        image = Image.open(BytesIO(data))
        return str(imagehash.phash(image))
    if media_type.startswith("video"):
        temp = DATA_DIR / "temp_video_hash"
        temp.write_bytes(data)
        cap = cv2.VideoCapture(str(temp))
        success, frame = cap.read()
        cap.release()
        temp.unlink(missing_ok=True)
        if not success:
            return None
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return str(imagehash.phash(image))
    return None


@app.post("/moderate")
def moderate(req: ModerateRequest) -> dict[str, Any]:
    t_score = text_score(req.text)
    m_score = media_score(req.media_url, req.media_type)
    score = max(t_score, m_score)
    if score < 0.4:
        decision = "SAFE"
    elif score < 0.7:
        decision = "REVIEW"
    else:
        decision = "BLOCK"
    return {"decision": decision, "score": score}


@app.post("/uniqueness")
def uniqueness(req: UniquenessRequest) -> dict[str, Any]:
    h = compute_hash(req.media_url, req.media_type)
    if not h:
        return {"score": 1.0}
    hashes = load_hashes()
    score = 1.0
    if h in hashes:
        score = 0.2
    else:
        hashes.append(h)
        save_hashes(hashes)
    return {"score": score}


@app.post("/feed")
def feed(req: FeedRequest) -> dict[str, Any]:
    return {"post_ids": []}
