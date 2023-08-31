from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import time_handeler
import sqlite3
import os
from inspect import getframeinfo, currentframe
from waitress import serve
import json
from all_config import getconfigs
from flask_cors import CORS
from time import time


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


def response_handeler(records):
    data = []
    for rec in records:
        current_timestamp = time()
        rec_data = {}
        if rec["time"] == "Tentative" and rec["timestamp"] < current_timestamp:
            continue
        for k, v in rec.items():
            if v == "":
                v = None
            if k in ["specs", "histories", "related"]:
                if v == "{}" or v == "":
                    rec_data[k] = None
                else:
                    if k == "specs":
                        new_specs = {}
                        specs = json.loads(v)
                        for skey, sval in specs.items():
                            new_key = skey.lower().replace(" ", "_")
                            new_specs[new_key] = sval

                        rec_data[k] = new_specs
                    elif k == "histories":
                        v = v.replace('""', 'null')
                        x = json.loads(v)
                        for not_knwo in x:
                            if "revised" in x[not_knwo].keys():
                                if x[not_knwo]['revised']:
                                    temp = x[not_knwo]['previous']
                                    x[not_knwo]['previous'] = x[not_knwo]['revised']
                                    x[not_knwo]['revised'] = temp
                        rec_data[k] = list(x.values())
                    else:
                        x = json.loads(v)
                        rec_data[k] = list(x.values())

            elif k == "eventid":
                rec_data[k] = int(v)
            else:
                rec_data[k] = v

        if rec_data["revised"]:
            temp = rec_data['previous']

            rec_data['previous'] = rec_data['revised']

            rec_data['revised'] = temp
        data.append(rec_data)
    return (data)


def db_connection():
    try:
        filename = getframeinfo(currentframe()).filename
        script_dir = os.path.dirname(os.path.abspath(filename))
        output_file = os.path.join(script_dir, output)
        connection = sqlite3.connect(f"file:{output_file}?mode=ro", uri=True)
        return connection
    except Exception as e:
        print('Something is wrong with db', e)


def fetch_data(connection, _from, _till):
    try:
        cursor = connection.cursor()
        cursor.row_factory = dict_factory
        sqlite_select_query = f"""SELECT * FROM my_table WHERE timestamp BETWEEN {_from} AND {_till} ORDER BY timestamp"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
    except Exception as e:
        print('Something is wrong with db', e)
    finally:
        if connection:
            connection.close()
        if records:
            return records
        else:
            print(f"now data was fetched {_from}, {_till}")


CONFIGS = getconfigs()
output = CONFIGS['files']['output']
app = Flask(__name__)
CORS(app)
api = Api(app)


class Timerange(Resource):
    def get(self):
        start = request.args.get('start')
        end = request.args.get('end')

        start_tuple = tuple(map(int, start.split('-')))
        end_tuple = tuple(map(int, end.split('-')))

        _from, _till = time_handeler.time_range(start_tuple, end_tuple)
        connection = db_connection()
        if connection:
            records = fetch_data(connection, _from, _till)
            data = response_handeler(records)
            return jsonify(data)


class Thisweek(Resource):
    def get(self):
        _from, _till = time_handeler.this_week()
        connection = db_connection()
        if connection:
            records = fetch_data(connection, _from, _till)
            data = response_handeler(records)
            return jsonify(data)


class Nextweek(Resource):
    def get(self):
        _from, _till = time_handeler.next_week()
        connection = db_connection()
        if connection:
            records = fetch_data(connection, _from, _till)
            data = response_handeler(records)
            return jsonify(data)


class Lastweek(Resource):
    def get(self):
        _from, _till = time_handeler.last_week()
        connection = db_connection()
        if connection:
            records = fetch_data(connection, _from, _till)
            data = response_handeler(records)
            return jsonify(data)


class Today(Resource):
    def get(self):
        _from, _till = time_handeler.today()
        connection = db_connection()
        if connection:
            records = fetch_data(connection, _from, _till)
            data = response_handeler(records)
            return jsonify(data)


class Tomorrow(Resource):
    def get(self):
        _from, _till = time_handeler.tomorrow()
        connection = db_connection()
        if connection:
            records = fetch_data(connection, _from, _till)
            data = response_handeler(records)
            return jsonify(data)


class Yesterday(Resource):
    def get(self):
        _from, _till = time_handeler.yesterday()
        connection = db_connection()
        if connection:
            records = fetch_data(connection, _from, _till)
            data = response_handeler(records)
            return jsonify(data)


class Thismonth(Resource):
    def get(self):
        _from, _till = time_handeler.this_month()
        connection = db_connection()
        if connection:
            records = fetch_data(connection, _from, _till)
            data = response_handeler(records)
            return jsonify(data)


class Nextmonth(Resource):
    def get(self):
        _from, _till = time_handeler.next_month()
        connection = db_connection()
        if connection:
            records = fetch_data(connection, _from, _till)
            data = response_handeler(records)
            return jsonify(data)


class Lastmonth(Resource):
    def get(self):
        _from, _till = time_handeler.last_month()
        connection = db_connection()
        if connection:
            records = fetch_data(connection, _from, _till)
            data = response_handeler(records)
            return jsonify(data)


for Resource, url in CONFIGS['resources'].items():
    api.add_resource(eval(Resource.capitalize()), url)

if __name__ == '__main__':
    serve(app, host=CONFIGS['flask']['host'], port=CONFIGS['flask']['port'])
