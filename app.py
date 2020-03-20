import base64
import hashlib
from Crypto.Cipher import AES, DES, DES3
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random
from flask import Flask, redirect, jsonify, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return redirect('/secrecy')


@app.route('/secrecy', methods=['GET', 'POST'])
def secrecy_view():
    if request.method == 'POST':
        data = request.get_json(silent=True)
    else:
        data = request.args
    result = secrecy(data)
    if result[0]:
        return jsonify({
            'code': 200,
            'msg': 'success',
            'data': result[1]
        })
    else:
        return jsonify({
            'code': 500,
            'msg': result[1],
            'data': None
        })


def secrecy(params):
    try:
        if params['type'] in ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'sha3_224', 'sha3_256', 'sha3_384',
                              'sha3_512', 'blake2b', 'blake2s', 'shake_128', 'shake_256']:
            return True, getattr(hashlib, params['type'])(params['text'].encode()).hexdigest()
        elif params['type'] == 'AES':
            if len(params['key']) > 32:
                return False, 'The \'key\' cannot be longer than 32'
            while len(params['key']) not in [16, 24, 32]:
                params['key'] += ' '
            while len(params['text']) % 32 != 0:
                params['text'] += ' '
            aes = AES.new(params['key'].encode("utf-8"), AES.MODE_ECB)
            return True, base64.encodebytes(aes.encrypt(params['text'].encode('utf-8'))).decode().rstrip('\n')
        elif params['type'] == 'D-AES':
            if len(params['key']) > 32:
                return False, 'The \'key\' cannot be longer than 32'
            while len(params['key']) not in [16, 24, 32]:
                params['key'] += ' '
            aes = AES.new(params['key'].encode("utf-8"), AES.MODE_ECB)
            return True, aes.decrypt(base64.decodebytes(params['text'].encode())).decode().rstrip(' ')
        elif params['type'] == 'DES':
            if len(params['key']) > 8:
                return False, 'The \'key\' cannot be longer than 8'
            while len(params['key']) < 8:
                params['key'] += ' '
            while len(params['text']) % 8 != 0:
                params['text'] += ' '
            des = DES.new(params['key'].encode("utf-8"), DES.MODE_ECB)
            return True, base64.encodebytes(des.encrypt(params['text'].encode('utf-8'))).decode().rstrip('\n')
        elif params['type'] == 'D-DES':
            if len(params['key']) > 8:
                return False, 'The \'key\' cannot be longer than 8'
            while len(params['key']) < 8:
                params['key'] += ' '
            des = DES.new(params['key'].encode("utf-8"), DES.MODE_ECB)
            return True, des.decrypt(base64.decodebytes(params['text'].encode())).decode().rstrip(' ')
        elif params['type'] == 'DES3':
            if len(params['key']) > 16:
                return False, 'The \'key\' cannot be longer than 16'
            while len(params['key']) < 16:
                params['key'] += ' '
            while len(params['text']) % 8 != 0:
                params['text'] += ' '
            des3 = DES3.new(params['key'].encode("utf-8"), DES3.MODE_ECB)
            return True, base64.encodebytes(des3.encrypt(params['text'].encode('utf-8'))).decode().rstrip('\n')
        elif params['type'] == 'D-DES3':
            if len(params['key']) > 16:
                return False, 'The \'key\' cannot be longer than 16'
            while len(params['key']) < 16:
                params['key'] += ' '
            des3 = DES3.new(params['key'].encode("utf-8"), DES3.MODE_ECB)
            return True, des3.decrypt(base64.decodebytes(params['text'].encode())).decode().rstrip(' ')
        elif params['type'] == 'rsa-k':
            length = params.get('length', '1024')
            if int(length) < 1024:
                length = "1024"
            password = params.get('password', None)
            if password == "":
                password = None
            x = RSA.generate(int(length), Random.new().read)
            s_key = x.export_key(passphrase=password, pkcs=8, protection="scryptAndAES128-CBC")
            g_key = x.publickey().export_key()
            return True, [s_key.decode(), g_key.decode()]
        elif params['type'] == 'rsa-e':
            password = params.get('password', None)
            if password == "":
                password = None
            g_key = PKCS1_v1_5.new(RSA.importKey(params['pub_k'], passphrase=password))
            en_data = g_key.encrypt(params['text'].encode())
            return True, base64.b64encode(en_data).decode()
        elif params['type'] == 'rsa-d':
            password = params.get('password', None)
            if password == "":
                password = None
            s_key = PKCS1_v1_5.new(RSA.importKey(params['pri_k'], passphrase=password))
            de_data = s_key.decrypt(base64.b64decode(params['text']), Random.new().read).decode()
            return True, de_data
        else:
            return False, 'params error'
    except Exception as ex:
        return False, str(ex)


if __name__ == '__main__':
    app.run()
