from fastapi import FastAPI
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io
from fastapi.responses import StreamingResponse
from pathlib import Path

app = FastAPI()

class NewsSummary(BaseModel):
    text: str

@app.post("/generate")
async def generate_image(data: NewsSummary):
    text = data.text

    # ✅ 이미지 생성
    img = Image.new("RGB", (1080, 1080), color="white")
    draw = ImageDraw.Draw(img)

    # ✅ 폰트 경로 설정 (같은 디렉토리에 fonts 폴더 만들고 .ttf 넣기)
    font_path = Path(__file__).parent / "fonts" / "나눔손글씨 다시 시작해.ttf"
    try:
        font = ImageFont.truetype(str(font_path), size=36)
    except Exception as e:
        print(f"폰트 로드 오류: {e}")
        font = ImageFont.load_default()

    # ✅ 텍스트 줄바꿈
    lines = textwrap.wrap(text, width=35)
    y_text = 100
    for line in lines:
        draw.text((100, y_text), line, font=font, fill="black")
        y_text += 50

    # ✅ 이미지 반환
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")
