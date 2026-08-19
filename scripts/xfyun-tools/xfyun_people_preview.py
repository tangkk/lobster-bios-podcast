#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import base64
import hashlib
import hmac
import json
import os
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import websocket


def auth_url(ws_url: str, api_key: str, api_secret: str) -> str:
    host = ws_url.split('://', 1)[1].split('/', 1)[0]
    path = '/' + ws_url.split('://', 1)[1].split('/', 1)[1]
    date = format_date_time(mktime(datetime.now().timetuple()))
    sign_origin = f"host: {host}\ndate: {date}\nGET {path} HTTP/1.1"
    sign_sha = hmac.new(api_secret.encode(), sign_origin.encode(), digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(sign_sha).decode()
    auth_origin = f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{sign}"'
    auth = base64.b64encode(auth_origin.encode()).decode()
    return ws_url + "?" + urlencode({"host": host, "date": date, "authorization": auth})


def synth(text: str, out_path: str, voice: str, speed: int, volume: int, pitch: int, ws_url: str):
    appid = os.environ.get("XFYUN_APPID", "")
    apikey = os.environ.get("XFYUN_API_KEY", "")
    apisecret = os.environ.get("XFYUN_API_SECRET", "")
    if not (appid and apikey and apisecret):
        raise RuntimeError("Missing XFYUN_APPID/XFYUN_API_KEY/XFYUN_API_SECRET")

    url = auth_url(ws_url, apikey, apisecret)
    if os.path.exists(out_path):
        os.remove(out_path)

    payload = {
        "header": {"app_id": appid, "status": 2},
        "parameter": {
            "tts": {
                "vcn": voice,
                "volume": volume,
                "rhy": 0,
                "speed": speed,
                "pitch": pitch,
                "bgs": 0,
                "reg": 0,
                "rdn": 0,
                "audio": {
                    "encoding": "lame",
                    "sample_rate": 24000,
                    "channels": 1,
                    "bit_depth": 16,
                    "frame_size": 0,
                },
            }
        },
        "payload": {
            "text": {
                "encoding": "utf8",
                "compress": "raw",
                "format": "plain",
                "status": 2,
                "seq": 0,
                "text": base64.b64encode(text.encode("utf-8")).decode("utf-8"),
            }
        },
    }

    done = {"ok": False, "err": None}

    def on_message(ws, message):
        try:
            msg = json.loads(message)
            code = msg.get("header", {}).get("code", -1)
            if code != 0:
                done["err"] = f"code={code}, msg={msg.get('header', {}).get('message')}"
                ws.close()
                return
            audio = msg.get("payload", {}).get("audio", {})
            b64 = audio.get("audio", "")
            if b64:
                with open(out_path, "ab") as f:
                    f.write(base64.b64decode(b64))
            if audio.get("status") == 2:
                done["ok"] = True
                ws.close()
        except Exception as e:
            done["err"] = str(e)
            ws.close()

    def on_error(ws, error):
        done["err"] = str(error)

    def on_open(ws):
        ws.send(json.dumps(payload, ensure_ascii=False))

    ws = websocket.WebSocketApp(url, on_message=on_message, on_error=on_error)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    if done["err"]:
        raise RuntimeError(done["err"])
    if not done["ok"]:
        raise RuntimeError("TTS did not complete")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default="x6_lingfeiyi_pro")
    ap.add_argument("--speed", type=int, default=46)
    ap.add_argument("--volume", type=int, default=52)
    ap.add_argument("--pitch", type=int, default=48)
    ap.add_argument("--url", default="wss://cbm01.cn-huabei-1.xf-yun.com/v1/private/mcd9m97e6")
    ap.add_argument("--text", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    synth(args.text, args.out, args.voice, args.speed, args.volume, args.pitch, args.url)
    print("OK:", args.out)
