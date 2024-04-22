from PIL import Image, ImageFont, ImageDraw
from collections.abc import Sequence
import qrcode

def make_QR(barcode: str, max_px: int) -> Image.Image:
    # QRのバージョン
    qr_version = 1
    # QRコードのセルの数 (バージョン依存)
    qr_cell_n = 21
    # 余白のセルの数
    border = 2
    # セルのサイズ
    box_size = max_px // (qr_cell_n + 2 * border)

    qr = qrcode.QRCode(
        version=qr_version,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(barcode)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img.convert("L")

def make_texts(texts: Sequence[str], height: int = 128, padding: int = 4, fontsize: int = 22) -> Image.Image:
    font = ImageFont.truetype(r'c:\WINDOWS\Fonts\UDDIGIKYOKASHON-R.TTC', fontsize)
    # 十分な広さの画像
    img = Image.new("L", (max(map(len, texts)) * fontsize * 2, 128))
    img.paste((256,), (0, 0, img.size[0], img.size[1]))
    draw = ImageDraw.Draw(img)
    draw.multiline_text((padding,padding), "\n".join(texts), "black", spacing=padding, font=font)
    bbox = draw.multiline_textbbox((padding, padding), "\n".join(texts), spacing=padding, font=font)
    rightside = bbox[2]
    right_edge = min(rightside + padding, img.size[0])
    return img.crop((0, 0, right_edge, height))

def make_image(barcode_text: str, texts: Sequence[str], height: int) -> Image.Image:
    qr_image = make_QR(barcode_text, height)
    text_image = make_texts(texts, height=height)
    
    img = Image.new("L", (height + text_image.size[0], height))
    pad_qr_image =  height - qr_image.size[1]
    img.paste((255,), (0, 0, img.size[0], img.size[1]))
    img.paste(qr_image, (pad_qr_image // 2, pad_qr_image//2))
    img.paste(text_image, (height, 0))
    return img

