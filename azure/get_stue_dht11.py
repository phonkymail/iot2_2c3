import sqlite3
from datetime import datetime
from time import sleep

def get_stue_data(number_of_rows):
        query = """SELECT * FROM room_1 ORDER BY datetime DESC;"""
        datetimes = []
        temperatures = []
        humidities = []
        try: # Connect to the SQLite database
            conn = sqlite3.connect('database/sensor_data.db')
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchmany(number_of_rows)
            print(rows)
            for row in rows:
                 datetimes.append(row[0])
                 temperatures.append(row[1])
                 humidities.append(row[2])
            conn.commit()
            return datetimes, temperatures, humidities
        
        except sqlite3.Error as sql_e:
            print(f"sqlite error occurred: {sql_e}")
            conn.rollback()
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            conn.close()


get_stue_data(20)