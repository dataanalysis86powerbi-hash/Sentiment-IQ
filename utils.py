import logging
import pandas as pd
import sqlite3
import threading
import time
import os

# Configuración de Logs (Sistemas Operativos)
logging.basicConfig(
    filename='system.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def registrar_log(mensaje):
    """Registra eventos en system.log"""
    logging.info(mensaje)

def exportar_csv(db_name="sentiment_iq.db", output_file="reporte_sentimientos.csv"):
    """File System: Exporta la base de datos a CSV"""
    try:
        conn = sqlite3.connect(db_name)
        df = pd.read_sql_query("SELECT * FROM reviews", conn)
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        conn.close()
        registrar_log(f"Reporte CSV generado: {output_file}")
        print(f"\n>>> Éxito: Reporte guardado como '{output_file}'")
    except Exception as e:
        registrar_log(f"Error al exportar CSV: {e}")
        print(f"Error al exportar: {e}")

def exportar_excel(db_name="sentiment_iq.db", output_file="reporte_sentimientos.xlsx"):
    """File System: Exporta la base de datos a Excel (.xlsx)"""
    try:
        conn = sqlite3.connect(db_name)
        df = pd.read_sql_query("SELECT * FROM reviews", conn)
        df.to_excel(output_file, index=False, engine='openpyxl')
        conn.close()
        registrar_log(f"Reporte Excel generado: {output_file}")
        print(f"\n>>> Éxito: Reporte guardado como '{output_file}'")
    except Exception as e:
        registrar_log(f"Error al exportar Excel: {e}")
        print(f"Error al exportar a Excel: {e}")

def tarea_respaldo():
    """Concurrencia: Simula un backup en un hilo secundario"""
    registrar_log("Iniciando tarea de respaldo de seguridad...")
    time.sleep(3) # Simulación de proceso pesado
    registrar_log("Respaldo completado exitosamente.")
    print("\n[HILO] Backup de seguridad finalizado en segundo plano.")

def iniciar_backup_hilo():
    """Lanza el hilo de respaldo"""
    hilo = threading.Thread(target=tarea_respaldo)
    hilo.daemon = True # El programa no esperará a que el hilo termine para cerrarse
    hilo.start()
