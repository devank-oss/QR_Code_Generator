from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, HttpUrl
from io import BytesIO
import qrcode
import base64

app = FastAPI()

templates = Jinja2Templates(directory="templates")


class QRRequest(BaseModel):
    url: HttpUrl


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.post("/qr")
async def generate_qr(data: QRRequest):

    website_url = str(data.url)

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(website_url)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    buffer = BytesIO()
    img.save(buffer, format="PNG")

    img_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return {
        "success": True,
        "qr_code": img_base64
    }