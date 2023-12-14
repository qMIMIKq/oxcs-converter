import logging
import os

import requests
from flask import Flask, request, Response
from pdf2image import convert_from_path
from waitress import serve

from modules.config import config
from modules.converter import DXF2IMG

FILES_DEST = './assets/uploads/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = FILES_DEST
first = DXF2IMG()


@app.route('/', methods=['GET'])
def index():
    return 'HELLO WORLD'


@app.route('/dxf-convert', methods=['POST'])
def dxf_converter():
    file = request.files['file']
    print(file.filename)
    save_path = f'{FILES_DEST}{file.filename}'
    file.save(os.path.join(save_path))
    first.convert_dxf2img([save_path], img_format='.png')
    with open(f'{save_path[:-4]}.png', 'rb') as f:
        resp = {
            "files": f
        }
        print(f.name)
        requests.post(url=f'{config.get("app_addr")}/api/files/save-files',
                      files=resp)
        print('file sending back')
        try:
            os.remove(os.path.join(save_path))
            os.remove(f'{os.path.join(save_path)[:-4]}.png')
        except:
            print('err')

        return Response(status=200)


@app.route('/pdf-convert', methods=['POST'])
def pdf_converter():
    file = request.files['file']
    print(file.filename)
    save_path = f'{FILES_DEST}{file.filename}'
    file.save(os.path.join(save_path))
    pages = convert_from_path(save_path)
    pages[0].save(f'{save_path[:-4]}.png', 'PNG')

    with open(f'{save_path[:-4]}.png', 'rb') as f:
        resp = {
            "files": f
        }

        requests.post(url=f'{config.get("app_addr")}/api/files/save-files',
                      files=resp)
        print('file sending back')
        try:
            os.remove(os.path.join(save_path))
            os.remove(f'{os.path.join(save_path)[:-4]}.png')
        except:
            print('err')
        return Response(status=200)


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5001)
    serve(app, host="0.0.0.0", port=5000)
