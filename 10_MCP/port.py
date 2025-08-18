from flask import Flask,jsonify
import os
from pyngrok import conf,ngrok
from flask_cors import CORS
conf.get_default().ngrok_path = r"C:\ngrok\ngrok.exe"

NGROK_AUTH_TOKEN='31CMhgdiUArvqdWEZWIvW6lM8nF_4YUHqGkdUdyrYkEfmgnbm'

app = Flask(__name__)
CORS(app)


@app.route('/api/hello',methods=['GET'])
def hello():
    return jsonify({'message':'hello from Mac via Terminal'})


if __name__=='__main__':
    port = 7001
    os.environ['FLASK_ENV'] = 'development'

    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    public_url = ngrok.connect(port)
    print(f"Public URL:{public_url}/api/hello \n \n")

    app.run(port=port)