# PROCESAMIENTO DE DATOS
from pathlib import Path
import pandas as pd
import utils

def cargar_estacionamientosDB():

    try:
     excel_path = Path('datos_entrada/BD_10_12_25_estacionamiento.xlsx')
     df_est_carros = pd.read_excel(excel_path, sheet_name=0)  # Primera hoja: carros
     df_est_motos = pd.read_excel(excel_path, sheet_name=1)   # Segunda hoja: motos
     df_est_parqueaderos = pd.read_excel(excel_path, sheet_name=2)  # Tercera hoja: parqueaderos
     
     # Crear una copia de cada uno
     df_carros_cargado = df_est_carros[["plate", "timestamp", "codigo", "tipo_dia", "sector"]].copy()
     df_motos_cargado = df_est_motos[["HORA", "LADO MANZANA", "PLACA", "sector", "tipo_dia"]].copy()
     df_parqueaderos_cargado = df_est_parqueaderos[["Placa","Placa_Mayus", "Tipo(Entrada/Salida)", "FechaHora", "tipo_dia", "sector", "cap_capacidad_autos", "cap_capacidad_motos"]].copy()
     
     return df_carros_cargado, df_motos_cargado, df_parqueaderos_cargado
     
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        raise

def cargar_capacidadesDB():
   
    try:
     excel_path = Path('datos_entrada/20251211_BD_capacidades.xlsx')
     df_capacidades = pd.read_excel(excel_path)
     return df_capacidades
     
    except Exception as e:
        print(f"Error al definir la ruta del archivo: {e}")
        raise
   
def procesar_autos(df_autos):

    # Convertir TIMESTAMP a datetime y crear columnas DIA y HORA
    df_autos["timestamp"] = pd.to_datetime(df_autos["timestamp"])
    df_autos["DIA"] = df_autos["timestamp"].dt.date
    df_autos["HORA"] = df_autos["timestamp"].dt.strftime("%H:%M")

    #tipo de dia
    df_autos['DIA_SEMANA'] = df_autos['timestamp'].dt.dayofweek
    df_autos['TIPO_DIA_CALC'] = df_autos['DIA_SEMANA'].apply(utils.clasificar_dia)

    # Renombrar y reordenar columnas 
    df_autos.rename(columns={"plate": "PLACA", "codigo": "CODIGO_MANZANA", "tipo_dia": "TIPO_DIA", "sector": "ZONA"}, inplace=True)
    df_autos_procesado = df_autos[["DIA", "HORA", "PLACA", "CODIGO_MANZANA", "TIPO_DIA", "ZONA", "DIA_SEMANA", "TIPO_DIA_CALC"]].copy()
    return df_autos_procesado

def procesar_motos(df_motos):

    # Convertir TIMESTAMP a datetime y crear columnas DIA y HORA
    df_motos["HORA"] = pd.to_datetime(df_motos["HORA"])
    df_motos["DIA"] = df_motos["HORA"].dt.date
    df_motos["HORA"] = df_motos["HORA"].dt.strftime("%H:%M")

    #tipo de dia
    df_motos['DIA_SEMANA'] = pd.to_datetime(df_motos["DIA"]).dt.dayofweek
    df_motos['TIPO_DIA_CALC'] = df_motos['DIA_SEMANA'].apply(utils.clasificar_dia)

    # Renombrar y reordenar columnas 
    df_motos.rename(columns={"LADO MANZANA": "CODIGO_MANZANA", "tipo_dia": "TIPO_DIA", "sector": "ZONA"}, inplace=True)
    df_motos_procesado = df_motos[["DIA", "HORA", "PLACA", "CODIGO_MANZANA", "TIPO_DIA", "ZONA", "DIA_SEMANA", "TIPO_DIA_CALC"]].copy()

    return df_motos_procesado

def procesar_parqueaderos(df_parqueaderos):

    # Convertir TIMESTAMP a datetime y crear columnas DIA y HORA
    df_parqueaderos["FechaHora"] = pd.to_datetime(df_parqueaderos["FechaHora"])
    df_parqueaderos["DIA"] = df_parqueaderos["FechaHora"].dt.date
    df_parqueaderos["HORA"] = df_parqueaderos["FechaHora"].dt.strftime("%H:%M")

    #tipo de dia
    df_parqueaderos['DIA_SEMANA'] = df_parqueaderos['FechaHora'].dt.dayofweek
    df_parqueaderos['TIPO_DIA_CALC'] = df_parqueaderos['DIA_SEMANA'].apply(utils.clasificar_dia)

    #tipo de vehiculo
    df_parqueaderos['TIPO_VEHICULO'] = df_parqueaderos['Placa'].apply(utils.clasificar_vehiculo_placa)

    # Renombrar y reordenar columnas 
    df_parqueaderos.rename(columns={"Placa_Mayus": "PLACA", "Tipo(Entrada/Salida)": "TIPO_ENT_SAL", "tipo_dia": "TIPO_DIA", "sector": "ZONA", "cap_capacidad_autos": "CAPACIDAD_AUTOS", "cap_capacidad_motos": "CAPACIDAD_MOTOS"}, inplace=True)
    df_parqueaderos_procesado = df_parqueaderos[["DIA", "HORA", "PLACA", "TIPO_DIA", "ZONA",  "TIPO_ENT_SAL",  "CAPACIDAD_AUTOS", "CAPACIDAD_MOTOS", "TIPO_VEHICULO","DIA_SEMANA", "TIPO_DIA_CALC"]].copy()

    return df_parqueaderos_procesado
 
def procesar_capacidadesDB(df_capacidades):

    df_cap_procesado = df_capacidades[["Codigo Bateria", "Zona", "Capacidad de motos", "Capacidad de autos"]].copy()
    
    # Renombrar y reordenar columnas
    df_cap_procesado.rename(columns={"Codigo Bateria": "CODIGO_MANZANA", "Zona": "ZONA", "Capacidad de autos": "CAPACIDAD_AUTOS", "Capacidad de motos": "CAPACIDAD_MOTOS"}, inplace=True)
    df_capacidades_procesado = df_cap_procesado[["CODIGO_MANZANA", "ZONA", "CAPACIDAD_AUTOS", "CAPACIDAD_MOTOS"]].copy()

    return df_capacidades_procesado
 
def obtener_zonas_unicas(df_autos, df_motos, df_capacidades):
 # Zonas únicas
    zonas_autos = set(df_autos['ZONA'].dropna().unique()) if df_autos is not None else set()
    zonas_motos = set(df_motos['ZONA'].dropna().unique()) if df_motos is not None else set()
    zonas_cap = set(df_capacidades['ZONA'].dropna().unique()) if df_capacidades is not None else set()
    zonas = sorted(list(zonas_autos | zonas_motos | zonas_cap))

    return zonas