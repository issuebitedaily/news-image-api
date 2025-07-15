from fastapi import FastAPI, Request
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io
from fastapi.responses import StreamingResponse

app = FastAPI()

class NewsSummary(BaseModel):
    text: str

@app.post("/generate")
async def generate_image(data: NewsSummary):
    text = data.text
    img = Image.new("RGB", (1080, 1080), color="white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("Arial.ttf", size=36)
    except:
        font = ImageFont.load_default()
    lines = textwrap.wrap(text, width=35)
    y_text = 100
    for line in lines:
        draw.text((100, y_text), line, font=font, fill="black")
        y_text += 50
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")