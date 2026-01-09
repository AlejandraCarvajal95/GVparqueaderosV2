# PROCESAMIENTO DE DATOS
from pathlib import Path
import pandas as pd
import utils

def cargar_estacionamientosDB(path):

    try:
     excel_path = Path(path)
     df_est_carros = pd.read_excel(excel_path, sheet_name=0)  # Primera hoja: carros
     df_est_motos = pd.read_excel(excel_path, sheet_name=1)   # Segunda hoja: motos
     df_est_parqueaderos = pd.read_excel(excel_path, sheet_name=2)  # Tercera hoja: parqueaderos
     
     # Crear una copia de cada uno
     df_carros_cargado = df_est_carros[["plate", "timestamp", "codigo", "tipo_dia", "sector"]].copy()
     df_motos_cargado = df_est_motos[["HORA", "LADO MANZANA", "PLACA", "sector", "tipo_dia"]].copy()
     df_parqueaderos_cargado = df_est_parqueaderos[["Placa","Placa_Mayus", "Tipo(Entrada/Salida)", "FechaHora", "tipo_dia", "sector", "cap_capacidad_autos", "cap_capacidad_motos", "Parqueadero"]].copy()

     return df_carros_cargado, df_motos_cargado, df_parqueaderos_cargado
     
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        raise

def cargar_capacidadesDB(path):
   
    try:
     excel_path = Path(path)
     df_capacidades = pd.read_excel(excel_path)
     return df_capacidades
     
    except Exception as e:
        print(f"Error al definir la ruta del archivo: {e}")
        raise
   
"""
def cargar_tasas_expansionDB(path):
   
    
    try:
        excel_path = Path(path)
        df_salidas = pd.read_excel(excel_path, sheet_name='F. Salidas', header=None)
        df_llegadas = pd.read_excel(excel_path, sheet_name='F. Llegadas', header=None)
        return df_salidas, df_llegadas
     
    except Exception as e:
        print(f"Error al cargar el archivo de tasas de expansión: {e}")
        raise
"""
   
def procesar_autos(df_autos):

    # Identificar placas de motos ANTES de procesar
    df_autos['TIPO_VEHICULO_CALC'] = df_autos['plate'].apply(utils.clasificar_vehiculo_placa)
    placas_motos_en_autos = df_autos[df_autos['TIPO_VEHICULO_CALC'] == 'MOTO']
    
    # Extraer registros de motos para transferir
    registros_motos_a_transferir = None
    if len(placas_motos_en_autos) > 0:
        # Preparar registros para transferir con estructura de df_motos
        registros_motos_a_transferir = placas_motos_en_autos[['timestamp', 'codigo', 'plate', 'sector', 'tipo_dia']].copy()
        registros_motos_a_transferir.rename(columns={
            'timestamp': 'HORA',
            'codigo': 'LADO MANZANA',
            'plate': 'PLACA'
        }, inplace=True)
        
        # Eliminar registros de motos del df de autos
        df_autos = df_autos[df_autos['TIPO_VEHICULO_CALC'] == 'AUTO'].copy()

    # Convertir TIMESTAMP a datetime y crear columnas DIA y HORA
    df_autos["timestamp"] = pd.to_datetime(df_autos["timestamp"])
    df_autos["DIA"] = df_autos["timestamp"].dt.date
    df_autos["HORA_COMPLETA"] = df_autos["timestamp"]  # Guardar timestamp completo para duraciones
    df_autos["HORA"] = df_autos["timestamp"].dt.hour  # Para cálculos

    #tipo de dia
    df_autos['DIA_SEMANA'] = df_autos['timestamp'].dt.dayofweek
    df_autos['TIPO_DIA_CALC'] = df_autos['DIA_SEMANA'].apply(utils.clasificar_dia)
     
    # Renombrar y reordenar columnas 
    df_autos.rename(columns={"plate": "PLACA", "codigo": "CODIGO_MANZANA", "tipo_dia": "TIPO_DIA", "sector": "ZONA"}, inplace=True)
    df_autos_procesado = df_autos[["DIA", "HORA", "HORA_COMPLETA", "PLACA", "CODIGO_MANZANA", "TIPO_DIA", "ZONA", "DIA_SEMANA", "TIPO_DIA_CALC"]].copy()
    
    return df_autos_procesado, registros_motos_a_transferir

def procesar_motos(df_motos):

    # Convertir TIMESTAMP a datetime y crear columnas DIA y HORA
    df_motos["timestamp_temp"] = pd.to_datetime(df_motos["HORA"])
    df_motos["DIA"] = df_motos["timestamp_temp"].dt.date
    df_motos["HORA_COMPLETA"] = df_motos["timestamp_temp"]  # Guardar timestamp completo para duraciones
    df_motos["HORA"] = df_motos["timestamp_temp"].dt.hour  # Para cálculos como entero (maneja NaN automáticamente)


    #tipo de dia
    df_motos['DIA_SEMANA'] = pd.to_datetime(df_motos["DIA"]).dt.dayofweek
    df_motos['TIPO_DIA_CALC'] = df_motos['DIA_SEMANA'].apply(utils.clasificar_dia)

    # Eliminar placas de autos en la hoja de motos
    df_motos['TIPO_VEHICULO_CALC'] = df_motos['PLACA'].apply(utils.clasificar_vehiculo_placa)
    df_motos = df_motos[df_motos['TIPO_VEHICULO_CALC'] == 'MOTO'].copy()

    # Renombrar y reordenar columnas 
    df_motos.rename(columns={"LADO MANZANA": "CODIGO_MANZANA", "tipo_dia": "TIPO_DIA", "sector": "ZONA"}, inplace=True)
    df_motos_procesado = df_motos[["DIA", "HORA", "HORA_COMPLETA", "PLACA", "CODIGO_MANZANA", "TIPO_DIA", "ZONA", "DIA_SEMANA", "TIPO_DIA_CALC"]].copy()

    return df_motos_procesado

def procesar_parqueaderos(df_parqueaderos):

    # Convertir TIMESTAMP a datetime y crear columnas DIA y HORA
    df_parqueaderos["FechaHora"] = pd.to_datetime(df_parqueaderos["FechaHora"])
    df_parqueaderos["DIA"] = df_parqueaderos["FechaHora"].dt.date
    df_parqueaderos["HORA_COMPLETA"] = df_parqueaderos["FechaHora"]  # Guardar timestamp completo para duraciones
    df_parqueaderos["HORA"] = df_parqueaderos["FechaHora"].dt.hour  # Para cálculos

    #tipo de dia
    df_parqueaderos['DIA_SEMANA'] = df_parqueaderos['FechaHora'].dt.dayofweek
    df_parqueaderos['TIPO_DIA_CALC'] = df_parqueaderos['DIA_SEMANA'].apply(utils.clasificar_dia)

    #tipo de vehiculo
    df_parqueaderos['TIPO_VEHICULO'] = df_parqueaderos['Placa'].apply(utils.clasificar_vehiculo_placa)

    # Renombrar y reordenar columnas 
    df_parqueaderos.rename(columns={"Placa_Mayus": "PLACA", "Tipo(Entrada/Salida)": "TIPO_ENT_SAL", "Parqueadero": "PARQUEADERO", "tipo_dia": "TIPO_DIA", "sector": "ZONA", "cap_capacidad_autos": "CAPACIDAD_AUTOS", "cap_capacidad_motos": "CAPACIDAD_MOTOS"}, inplace=True)
    df_parqueaderos_procesado = df_parqueaderos[["DIA", "HORA", "HORA_COMPLETA", "PLACA", "TIPO_DIA", "ZONA",  "TIPO_ENT_SAL",  "CAPACIDAD_AUTOS", "CAPACIDAD_MOTOS", "TIPO_VEHICULO","DIA_SEMANA", "TIPO_DIA_CALC", "PARQUEADERO"]].copy()

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

"""
def calcular_datos_expandidos_via(df_procesado, tasas_salidas, tasas_llegadas, tipo_vehiculo):
   
    Calcula datos expandidos (entradas, salidas, ocupación) para horas 18-23.
    
    Args:
        df_procesado: DataFrame procesado de autos o motos
        tasas_salidas: Dict de tasas de salidas por zona/dia/hora
        tasas_llegadas: Dict de tasas de llegadas por zona/dia/hora
        tipo_vehiculo: 'AUTO' o 'MOTO'
    
    Returns:
        dict: {
            ('ZONA', 'TIPO_DIA'): {
                'entradas': {7: 50, ..., 17: 145, 18: 255, ...},
                'salidas': {7: 30, ..., 17: 80, 18: 141, ...},
                'ocupacion': {7: 20, ..., 17: 120, 18: 234, ...}
            }
        }

    import numpy as np
    
    resultado = {}
    
    # Agrupar por ZONA y TIPO_DIA
    for (zona, tipo_dia), grupo in df_procesado.groupby(['ZONA', 'TIPO_DIA_CALC']):
        
        fechas = grupo['DIA'].unique()
        horas_reales = sorted(grupo['HORA'].unique())
        
        entradas_por_hora = {}
        salidas_por_hora = {}
        ocupacion_por_hora = {}
        
        # Calcular datos REALES (promedio entre fechas)
        for hora in horas_reales:
            ocups, ents, sals = [], [], []
            
            for fecha in fechas:
                df_fecha = grupo[grupo['DIA'] == fecha]
                
                # Ocupación: placas únicas en esa hora
                placas = set(df_fecha[df_fecha['HORA'] == hora]['PLACA'].dropna().unique())
                ocups.append(len(placas))
                
                # Entradas y Salidas
                if hora > min(horas_reales):
                    placas_ant = set(df_fecha[df_fecha['HORA'] == hora - 1]['PLACA'].dropna().unique())
                    ents.append(len(placas - placas_ant))  # Placas nuevas
                    sals.append(len(placas_ant - placas))  # Placas que salieron
                else:
                    ents.append(len(placas))
                    sals.append(0)
            
            ocupacion_por_hora[hora] = round(sum(ocups) if ocups else 0)
            entradas_por_hora[hora] = round(sum(ents) if ents else 0)
            salidas_por_hora[hora] = round(sum(sals) if sals else 0)
        
        # EXPANDIR datos para horas 18-23
        ultima_hora_real = max(horas_reales)
        
        # Obtener tasas para esta zona/tipo_dia
        tasas_ent = tasas_llegadas.get(zona, {}).get(tipo_vehiculo, {}).get(tipo_dia, {})
        tasas_sal = tasas_salidas.get(zona, {}).get(tipo_vehiculo, {}).get(tipo_dia, {})
        
        # Valores base para expansión (última hora real)
        entradas_actual = entradas_por_hora.get(ultima_hora_real, 0)
        salidas_actual = salidas_por_hora.get(ultima_hora_real, 0)
        ocupacion_actual = ocupacion_por_hora.get(ultima_hora_real, 0)
        
        # Expandir sucesivamente
        for hora in range(18, 24):  # 18-23
            # Aplicar tasa de expansión
            tasa_ent = tasas_ent.get(hora, 1.0)
            tasa_sal = tasas_sal.get(hora, 1.0)
            
            entradas_actual = round(entradas_actual * tasa_ent)
            salidas_actual = round(salidas_actual * tasa_sal)
            
            # Ocupación acumulativa
            ocupacion_actual = round(ocupacion_actual + entradas_actual - salidas_actual)
            
            # Guardar valores expandidos
            entradas_por_hora[hora] = entradas_actual
            salidas_por_hora[hora] = salidas_actual
            ocupacion_por_hora[hora] = max(0, ocupacion_actual)  # No puede ser negativa
        
        # Guardar resultado
        resultado[(zona, tipo_dia)] = {
            'entradas': entradas_por_hora,
            'salidas': salidas_por_hora,
            'ocupacion': ocupacion_por_hora
        }
    
    return resultado
"""
"""
def procesar_tasas_expansion(df_salidas, df_llegadas):
    
    Procesa los DataFrames de tasas de expansión y retorna un diccionario estructurado.
    
    Args:
        df_salidas: DataFrame con datos de la hoja 'F. Salidas' (header=None)
        df_llegadas: DataFrame con datos de la hoja 'F. Llegadas' (header=None)
    
    Returns:
        dict: Estructura {
            'salidas': {
                'ZONA': {
                    'AUTO': {'TIPICO': {18: 1.05, 19: 1.12, ...}, 'SABADO': {...}, 'DOMINGO': {...}},
                    'MOTO': {'TIPICO': {...}, 'SABADO': {...}, 'DOMINGO': {...}}
                }
            },
            'llegadas': { ... misma estructura ... }
        }
 
    resultado = {
        'salidas': _extraer_datos_tasa(df_salidas),
        'llegadas': _extraer_datos_tasa(df_llegadas)
    }
    
    return resultado

"""
"""
def _extraer_datos_tasa(df):
  
    Extrae datos de una hoja de tasas (Salidas o Llegadas).
    Solo toma datos desde columna 15 (tasas de expansión) y horas 6pm-11pm.
    
    Args:
        df: DataFrame con header=None
    
    Returns:
        dict: Estructura {ZONA: {TIPO_VEH: {TIPO_DIA: {hora: valor}}}}
   
    resultado = {}
    
    # Fila 1: Zonas (columnas donde aparecen - celdas combinadas)
    # Fila 2: Tipo de vehículo (celdas combinadas)
    # Fila 3: Tipo de día (Dom, Sáb, Típ)
    # Fila 4+: Horas con datos
    
    # Mapeo de nombres
    tipo_dia_map = {'Dom': 'DOMINGO', 'Sáb': 'SABADO', 'Típ': 'TIPICO'}
    tipo_veh_map = {'Autos': 'AUTO', 'Motos': 'MOTO'}
    
    # Propagar valores de celdas combinadas (ffill) en filas 1 y 2
    # Desde columna 1 (col 0 son las etiquetas de hora)
    df_temp = df.copy()
    df_temp.iloc[1, 1:] = df_temp.iloc[1, 1:].ffill()  # Zonas
    df_temp.iloc[2, 1:] = df_temp.iloc[2, 1:].ffill()  # Tipo vehículo
    
    # Extraer estructura de columnas (empezar desde columna 1)
    for col in range(1, df_temp.shape[1]):
        zona = df_temp.iloc[1, col]
        tipo_veh = df_temp.iloc[2, col]
        tipo_dia = df_temp.iloc[3, col]
        
        # Saltar columnas vacías
        if pd.isna(zona) or pd.isna(tipo_veh) or pd.isna(tipo_dia):
            continue
        
        # Normalizar nombres
        zona = str(zona).strip().upper()
        if 'PERRO' in zona:
            zona = 'SAN FERNANDO (PARQUE DEL PERRO)'
        elif 'CENTENARIO' in zona:
            zona = 'CENTENARIO'
        elif 'PEÑON' in zona or 'PENON' in zona:
            zona = 'EL PEÑON'
        elif 'GRANADA' in zona:
            zona = 'GRANADA'
        elif 'ANTONIO' in zona:
            zona = 'SAN ANTONIO'
        
        tipo_veh_norm = tipo_veh_map.get(tipo_veh, tipo_veh)
        tipo_dia_norm = tipo_dia_map.get(tipo_dia, tipo_dia)
        
        # Inicializar estructura
        if zona not in resultado:
            resultado[zona] = {}
        if tipo_veh_norm not in resultado[zona]:
            resultado[zona][tipo_veh_norm] = {}
        if tipo_dia_norm not in resultado[zona][tipo_veh_norm]:
            resultado[zona][tipo_veh_norm][tipo_dia_norm] = {}
        
        # Extraer datos por hora - SOLO 6 PM a 11 PM (filas 15-20)
        for row in range(15, 21):  # Filas 15-20 son 6pm-11pm
            hora_str = df_temp.iloc[row, 0]
            valor = df_temp.iloc[row, col]
            
            if pd.isna(hora_str) or pd.isna(valor):
                continue
            
            # Convertir hora a número (6 p. m. → 18, etc.)
            hora_num = _convertir_hora_a_numero(hora_str)
            
            # Verificar que esté en rango 18-23 (6pm-11pm)
            if hora_num < 18 or hora_num > 23:
                continue
            
            # Guardar valor (convertir a float y redondear a 2 decimales)
            try:
                resultado[zona][tipo_veh_norm][tipo_dia_norm][hora_num] = round(float(valor), 2)
            except (ValueError, TypeError):
                pass
    
    return resultado
 """
"""
def _convertir_hora_a_numero(hora_str):
   
    Convierte formato '7 a. m.' o '12 p. m.' a número de hora (0-23).
    
    Args:
        hora_str: String con formato de hora
    
    Returns:
        int: Hora en formato 24h
   
    hora_str = str(hora_str).strip().lower()
    
    # Reemplazar espacio no-rompible (\xa0) por espacio normal
    hora_str = hora_str.replace('\xa0', ' ')
    
    # Extraer número
    import re
    match = re.search(r'(\d+)', hora_str)
    if not match:
        return 0
    
    hora = int(match.group(1))
    
    # Ajustar AM/PM
    if 'p. m.' in hora_str or 'p.m.' in hora_str or 'pm' in hora_str or 'p. m' in hora_str:
        if hora != 12:
            hora += 12
    elif hora == 12 and ('a. m.' in hora_str or 'a.m.' in hora_str or 'am' in hora_str):
        hora = 0
    
    return hora
"""