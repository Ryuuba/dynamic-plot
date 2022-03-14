from cProfile import label
import imp
from optparse import Values
from flask import Flask, Response, render_template, stream_with_context, request
import db_conn.sqlite3_conn as sqlite3_conn
from datetime import datetime
import tzlocal
import json
import time
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

def update_readings():
    if request.headers.getlist('X-Forwarded-For'):
        client_ip = request.headers.getlist('X-Forwarded-For')[0]
    else:
        client_ip = request.remote_addr or ''
    try:
        logger.info("Client %s connected", client_ip)
        while True:
            db_conn = sqlite3_conn.create_connection('./data/test.db')
            c722_data = sqlite3_conn.get_last_data(db_conn, 1, 'C722')
            c722_time = datetime.fromtimestamp(
                    c722_data[0][0], tzlocal.get_localzone()
                    ).strftime('%H:%M:%S')
            c722_val = c722_data[0][2]
            labred_data = sqlite3_conn.get_last_data(db_conn, 1, 'LabRed')
            labred_time = datetime.fromtimestamp(
                    labred_data[0][0], tzlocal.get_localzone()
                    ).strftime('%H:%M:%S')
            labred_val = labred_data[0][2]
            print('C722time: {}, C722value: {}'.format(c722_time, c722_val))
            print('LabRedtime: {}, LabRedvalue: {}'.format(labred_time, labred_val))
            db_conn.close()
            json_data = json.dumps(
                {
                    'C722time': c722_time, 
                    'C722value': c722_val,
                    'C722title': 'C722 CO2 level [ppm]',
                    'C722color': 'rgb(0, 128, 128)',
                    'LabRedtime': labred_time, 
                    'LabRedvalue': labred_val,
                    'LabRedtitle': 'LabRed CO2 level [ppm]',
                    'LabRedcolor': 'rgb(255, 127, 127)'
                }
            )
            yield f'data:{json_data}\n\n'
            time.sleep(30)
    except GeneratorExit:
        logger.info("Client %s disconnected", client_ip)

@app.route('/')
def home():
    return render_template('graphs.html')

@app.route('/chart-data')
def chart_data():
    response = Response(
        stream_with_context(update_readings()), mimetype = 'text/event-stream'
    )
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['X-Accel-Buffering'] = 'no'
    return response

if __name__ == '__main__':
    print('Start server...')
    app.run(host = '0.0.0.0', threaded=True, debug = True)
