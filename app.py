from cProfile import label
from optparse import Values
from flask import Flask, render_template
import db_conn.sqlite3_conn as sqlite3_conn
from datetime import datetime
import tzlocal

app = Flask(__name__)

@app.route('/')
def home():
    db_conn = sqlite3_conn.create_connection('./data/test.db')
    data = sqlite3_conn.get_last_data(db_conn, 10, 'C722')
    time_label = [
        datetime.fromtimestamp(
            row[0], tzlocal.get_localzone()
            ).strftime('%H:%M:%S') for row in data
    ]
    c722_val = [row[2] for row in data]
    data = sqlite3_conn.get_last_data(db_conn, 10, 'LabRed')
    lab_red_val = [row[2] for row in data]
    return render_template(
        'graphs.html', 
        labels = time_label, 
        values = c722_val
    )

if __name__ == '__main__':
    app.run(debug=True, threaded=True)