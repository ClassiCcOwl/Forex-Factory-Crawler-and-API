from json import load
import os
from sqlite3 import connect
from inspect import getframeinfo, currentframe
from tqdm import tqdm
from datetime import datetime
from pytz import timezone
from all_config import getconfigs


def script_dir_finder():
    filename = getframeinfo(currentframe()).filename
    script_dir = os.path.dirname(os.path.abspath(filename))
    return script_dir


def json_reader(script_dir, json_file_name):
    input_file = os.path.join(script_dir, json_file_name)
    with open(input_file) as f:
        data = load(f)
        return data


def json_cleaner(script_dir, json_file_name):
    input_file = os.path.join(script_dir, json_file_name)
    with open(input_file, "w") as f:
        f.write('[]')


def output_maker(script_dir, data):
    output_file = os.path.join(script_dir, output)
    try:
        connection = connect(output_file)
        cursor = connection.cursor()
        table_columns = ", ".join(
            [f"{col['name']} {col['type']}" for col in schema['columns']])
        table_columns += ", PRIMARY KEY (eventid)"
        table_stmt = f"CREATE TABLE IF NOT EXISTS {schema['table_name']} ({table_columns})"
        cursor.execute(table_stmt)
        columns = [col['name'] for col in schema['columns']]
        placeholders = ", ".join(["?" for _ in columns])
        insert_stmt = f"INSERT OR REPLACE INTO {schema['table_name']} ({', '.join(columns)}) VALUES ({placeholders})"
        cursor.execute("BEGIN")
        batch_size = 1000
        datetime_NY = datetime.now(tz)
        for i in tqdm(range(0, len(data), batch_size), colour="yellow", desc=f"Inserting at {datetime_NY.strftime('%H:%M:%S')}"):
            batch_data = [tuple(record[col['name']] for col in schema['columns'])
                          for record in data[i:i+batch_size]]
            cursor.executemany(insert_stmt, batch_data)
        cursor.execute("COMMIT")
    except Exception as e:
        print('Something is wrong with db', e)
    finally:
        if connection:
            connection.close()


def db_do(json_file_name):
    script_dir = script_dir_finder()
    data = json_reader(script_dir, json_file_name)
    output_maker(script_dir, data)
    json_cleaner(script_dir, json_file_name)


CONFIGS = getconfigs()
tz = timezone(CONFIGS['times']['tehran.timezone'])
output = CONFIGS['files']['output']
schema = {
    "table_name": "my_table",
    "columns": [
        {"name": "eventid", "type": "TEXT", "primary_key": True},
        {"name": "timestamp", "type": "REAL"},
        {"name": "date", "type": "TEXT"},
        {"name": "time", "type": "TEXT"},
        {"name": "currency", "type": "TEXT"},
        {"name": "impact", "type": "TEXT"},
        {"name": "title", "type": "TEXT"},
        {"name": "actual", "type": "REAL"},
        {"name": "actualtype", "type": "TEXT"},
        {"name": "forecast", "type": "REAL"},
        {"name": "previous", "type": "REAL"},
        {"name": "previoustype", "type": "TEXT"},
        {"name": "specs", "type": "TEXT"},
        {"name": "histories", "type": "TEXT"},
        {"name": "related", "type": "TEXT"},
        {"name": "revised", "type": "TEXT"}
    ]
}
