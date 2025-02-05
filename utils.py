import base64
from io import BytesIO


def pil_to_b64(img) -> str:
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return img_b64
