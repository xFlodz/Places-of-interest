import qrcode
from io import BytesIO
import base64

from __init__ import db
from models import QRCode


def qrcode_generate(address):
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4
    )
    qr.add_data(f"https://places-of-interest.onrender.com//post/{address}")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    img_bytes = BytesIO()
    qr_img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

    existing_qr_code = QRCode.query.filter_by(post_id=address).first()

    if existing_qr_code:
        existing_qr_code.data = f"https://places-of-interest.onrender.com//post/{address}"
        existing_qr_code.image_base64 = img_base64
    else:
        new_qr_code = QRCode(data=f"https://places-of-interest.onrender.com//post/{address}", post_id=address,
                            image_base64=img_base64)
        db.session.add(new_qr_code)

    db.session.commit()
    return img_base64