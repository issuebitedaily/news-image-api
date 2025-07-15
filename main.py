from fastapi import FastAPI
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io
from fastapi.responses import StreamingResponse
from pathlib import Path

app = FastAPI()

# 전역 폰트 설정
font_path = Path(__file__).parent / "fonts" / "나눔손글씨 다시 시작해.ttf"
try:
    default_font = ImageFont.truetype(str(font_path), size=36)
except:
    default_font = ImageFont.load_default()

class NewsSummary(BaseModel):
    text: str

@app.post("/generate")
async def generate_image(data: NewsSummary):
    text = data.text
    img = Image.new("RGB", (1080, 1080), color="white")
    draw = ImageDraw.Draw(img)

    lines = textwrap.wrap(text, width=35)
    y_text = 100
    for line in lines:
        draw.text((100, y_text), line, font=default_font, fill="black")
        y_text += 50

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")
