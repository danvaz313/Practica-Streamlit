import sqlite3
import pandas as pd
from datetime import datetime
import os

class DataBase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        #Crear el directorio si no existe
        os.makedirs(os.path.dirname(self.db_path),exist_ok=True)
        self.inicializar_db()
        
    def inicializar_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                    CREATE TABLE IF NOT EXISTS lecturas_1 (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME, 
                    SENSOR TEXT,
                    VALOR REAL, 
                    ESTADO TEXT)
                    """)
            conn.execute("""
                    CREATE TABLE IF NOT EXISTS lecturas_2 (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME, 
                    SENSOR TEXT, 
                    VALOR REAL, 
                    ESTADO TEXT)
                    """)
            conn.execute("""
                    CREATE TABLE IF NOT EXISTS lecturas_3 (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME, 
                    SENSOR TEXT, 
                    VALOR REAL,
                    ESTADO TEXT)
                    """)
            conn.execute("""
                    CREATE TABLE IF NOT EXISTS lecturas_4 (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME, 
                    SENSOR TEXT, 
                    VALOR REAL,
                    ESTADO TEXT)
                    """)
    def guardar_lectura_air(self, sensor: str, air: float, estado:str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                    INSERT INTO lecturas_1(timestamp, SENSOR, VALOR, ESTADO)
                    VALUES (?, ?, ?, ?)
                        """, (datetime.now(), sensor, air, estado))
            
    def guardar_lectura_temp(self, sensor: str, temp: float, estado:str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                    INSERT INTO lecturas_2(timestamp, SENSOR,VALOR, ESTADO)
                    VALUES (?, ?, ?, ?)
                        """, (datetime.now(), sensor, temp, estado))

    def guardar_lectura_hum(self, sensor: str,hum: float, estado:str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                    INSERT INTO lecturas_3(timestamp, SENSOR, VALOR, ESTADO)
                    VALUES (?, ?, ?, ?)
                        """, (datetime.now(), sensor, hum, estado))
    
    def guardar_lectura_voc(self, sensor: str, voc: float, estado:str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                    INSERT INTO lecturas_4(timestamp, SENSOR, VALOR, ESTADO)
                    VALUES (?, ?, ?, ?)
                        """, (datetime.now(), sensor, voc, estado))
            
    def obtener_historico(self, sensor: str, limite: int = 1000) -> pd.DataFrame:
        
        if sensor == 'particulas':
            query = """
                SELECT timestamp, valor, estado
                FROM lecturas_1
                WHERE sensor = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """
        elif sensor == 'temperatura':
            query = """
                SELECT timestamp, valor, estado
                FROM lecturas_2
                WHERE sensor = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """
        elif sensor == 'humedad':
            query = """
                SELECT timestamp, valor, estado
                FROM lecturas_3
                WHERE sensor = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """
        elif sensor == 'cov':
            query = """
                SELECT timestamp, valor, estado
                FROM lecturas_4
                WHERE sensor = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """
        else:
            print("Error historico")
        
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query(query, conn, params=(sensor, limite))
