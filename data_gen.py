#!/usr/bin/python3
from numpy import random as rd
from sys import argv
import time
import db_conn.sqlite3_conn as sqlite3_conn

def main():
    db_path = argv[1]
    delay = float(argv[2])
    db_conn = sqlite3_conn.create_connection(db_path)
    location = ['C722', 'LabRed']
    try:
        while True:
            data_tuple = (
                str(int(time.time())),  # The current time (UNIX format)
                location[rd.randint(0, 2)], # The sensor location
                rd.randint(0, 10) + 400
            )
            print('Data tuple: {}'.format(data_tuple))
            sqlite3_conn.insert_tuple(db_conn, data_tuple)
            time.sleep(delay)
    except KeyboardInterrupt:
        print('\nDatabase connection is closed')
        db_conn.close()


if __name__ == '__main__':
    main()