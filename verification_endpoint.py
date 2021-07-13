from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk
import logging

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    content = request.get_json(silent=True)
    # signature = content["sig"]
    signature = content.get("sig")
    message = content["payload"]["message"]
    pk = content["payload"]["pk"]
    platform = content["payload"]["platform"]

    # Check platform
    if platform == 'Ethereum':
        # Check if signature is valid
        encoded_msg = eth_account.messages.encode_defunct(text=message)
        if eth_account.Account.recover_message(encoded_msg, signature=signature) == pk:
            result = True
        else:
            result = False
    elif platform == 'Algorand':
        # Check if signature is valid
        result = algosdk.util.verify_bytes(message.encode('utf-8'), signature, pk)
    else:
        result = False

    # result = True  # Should only be true if signature validates
    return jsonify(result)


if __name__ == '__main__':
    app.run(port='5002')
