import io
import os
import sys

from flask import request, Response, jsonify

from ascript.ios import system
from ascript.ios.developer.api import dao
from ascript.ios.developer.utils import env
from ascript.ios.developer.utils.env import get_asenv


current_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
# print(current_dir)
module_space = os.path.join(get_asenv()["home"], 'modules')

if not os.path.exists(module_space):
    os.makedirs(module_space)


def api(app):
    @app.route("/api/screen/capture", methods=['GET'])
    def api_screen_capture():
        if "device_id" in request.args:
            device_id = request.args["device_id"]
            print(device_id)
            client = env.get_client(device_id)
            print(client)
            image = client.screenshot()
            byte_arr = io.BytesIO()
            image.save(byte_arr, format='PNG')
            byte_arr = byte_arr.getvalue()
            return Response(byte_arr, mimetype='image/png')
        else:
            jsonify(dao.api_result(code=-1, msg="device_id"))





