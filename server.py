from flask import Flask, request
from decouple import config
import logging
import json
import hmac
import hashlib

FB_APP_SECRET = config('FB_APP_SECRET')
HUB_VERIFY_TOKEN = config('HUB_VERIFY_TOKEN')

log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)


def verify_signature(req, signature):
    payload = req.get_data()
    gen_signature = hmac.new(FB_APP_SECRET.encode('utf-8'), payload, hashlib.sha1).hexdigest()
    return hmac.compare_digest(signature, gen_signature)


def create_app(handle_comment_event):
    app = Flask(__name__)

    @app.route('/webhook', methods=['GET', 'POST'])
    def webhook():
        if request.method == 'GET':
            if request.args.get('hub.verify_token') == HUB_VERIFY_TOKEN:
                return request.args.get('hub.challenge')
            return 'Invalid token'
        elif request.method == 'POST':
            signature = request.headers.get('X-Hub-Signature').split('=')[1]
            if not verify_signature(request, signature):
                return 'Invalid request', 400

            data = json.loads(request.data)
            for entry in data['entry']:
                for event in entry['changes']:
                    if event['field'] == 'feed' and event['value']['item'] == 'comment':
                        handle_comment_event(event['value'])
            return 'OK', 200

    return app