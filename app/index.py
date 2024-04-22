import os
from .make_image import make_image
from flask import Flask, request, Response, stream_with_context
import json
from .printer import print as printer_print, get_printer_height
from collections.abc import Sequence

from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/Infogram/PTouch/PTouchPrint/', methods=["POST"])
def print_QR(): 
    printer_name = os.environ.get("PRINTERNAME", None)
    affiliation = os.environ.get("AFFILIATION", "[Affiliation dummy]")
    laboratory = os.environ.get("LABORATORY", "[Laboratory dummy]")

    printer_height_px = get_printer_height(printer_name)
    text_body = next(iter(request.form.keys()))

    for txt in text_body.split("$$$"):
        data = json.loads(txt)[0]

        barcode: str = data["BarcodeText"]
        texts: Sequence[str] = (
            affiliation,
            laboratory,
            barcode,
            data["FirstText"],
            data["SecondText"]
        )
        
        image = make_image(barcode, texts, printer_height_px)
        printer_print(image, printer_name)

        
    response = Response(response=stream_with_context("OK"), status=200)
    response.status_code = 200
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "text/plain" 
    return response
