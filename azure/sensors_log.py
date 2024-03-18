import sqlite3
from datetime import datetime
import paho.mqtt.subscribe as subscribe
import json

print("subscribe mqtt active")

def create_table():
    query = """CREATE TABLE IF NOT EXISTS room_1 (datetime TEXT NOT NULL, temperature REAL NOT NULL, humidity REAL NOT NULL);"""
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('database/sensor_data.db')
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except sqlite3.Error as sql_e:
        print(f"sqlite error occurred: {sql_e}")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()

create_table()

def on_message_print(client, userdata, message):
    query = """INSERT INTO room_1 (datetime, temperature, humidity) VALUES(?, ?, ?)"""
    now = datetime.now()
    now = now.strftime("%d/%m/%y %H:%M:%S")
    dht11_data = json.loads(message.payload.decode())
    data = (now, dht11_data['temperature'], dht11_data['humidity'])

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('database/sensor_data.db')
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
    except sqlite3.Error as sql_e:
        print(f"sqlite error occurred: {sql_e}")
        conn.rollback()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()
        userdata["message_count"] += 1
        if userdata["message_count"] >= 5:
            # it's possible to stop the program by disconnecting
            pass

subscribe.callback(on_message_print, "paho/test/topic", hostname="74.234.16.173", userdata={"message_count": 0})
