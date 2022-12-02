import time
import threading
import requests
import random
import logging
from flask import Flask
from flask_cors import CORS

# Imports the Cloud Logging client library
import google.cloud.logging
# Instantiates a client
client = google.cloud.logging.Client()
client.setup_logging()

app = Flask(__name__)
CORS(app)

def heavy_func():
    while True:
        secs = random.randint(5, 30)
        print("pausing for {} seconds".format(secs))
        time.sleep(random.randint(5, 30))
        cnt = random.randint(1,30)
        ms = random.randint(100,500)
        print("making {} requests with interval {}ms".format(cnt,ms))
        for x in range(cnt):
            try:
                print(".",end="")
                response = requests.get("http://35.188.38.77:80/",timeout=5)
                response.raise_for_status()
                logging.info("cloud-trace-demo-app-opentelemetry-client elapsed=%s",str(response.elapsed.total_seconds()))
       
                # time.sleep(ms/1000)
            except requests.exceptions.HTTPError as errh:
                print(errh)
            except requests.exceptions.ConnectionError as errc:
                print(errc)
            except requests.exceptions.Timeout as errt:
                print(errt)
            except requests.exceptions.RequestException as err:
                print(err)
        print("")


thread = threading.Thread(target=heavy_func)
thread.daemon = True         # Daemonize 
thread.start()

@app.route('/', methods=['GET'])
def get_method(): 
    return "work is in progress"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True),
