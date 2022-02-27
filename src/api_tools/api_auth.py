import urllib.parse
import hashlib
import hmac
import base64


def get_api_signature(url_path, data, secret):
    post_data = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + post_data).encode()
    message = url_path.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sig_digest = base64.b64encode(mac.digest())
    return sig_digest.decode()
