import shutil
import socket
import subprocess
from flask import Flask, render_template, jsonify, request


app = Flask(__name__)

def wifi_configure(ssid, password):
    try:
        wpaConfFile = '/etc/wpa_supplicant/wpa_supplicant.conf'
        shutil.copyfile(wpaConfFile, wpaConfFile + '.bkp')
        new_config = subprocess.check_output(['wpa_passphrase', ssid, password])
        with open(wpaConfFile, 'w+') as wpaFd:
            wpaFd.write("""
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

{}""".format(new_config))
    except Exception as e:
        print(e)

def get_ip():
    localSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        localSock.connect(('10.255.255.255', 1))
        localIp = localSock.getsockname()[0]
    except:
        localIp = '127.0.0.1'
    finally:
        localSock.close()
        return localIp

@app.route('/', strict_slashes=False, methods=['GET'])
def index():
    args = {
        'ip': get_ip(),
        'hostname': socket.gethostname()
    }
    return render_template('index.html', **args)

@app.route('/changeme', strict_slashes=False, methods=['POST'])
def process():
    try:
        if request.form['password'] and request.form['ssid']:
            wifi_configure(
                ssid=request.form['ssid'],
                password=request.form['password']
            )
    except Exception as e:
        response = jsonify({'status': 'error', 'message': "'{}'".format(e)})
        response.status_code = 404
        return response
    return index()

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=8000)
