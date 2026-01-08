import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import utils
import numpy as np

def calcular_ocupacion_via(df_procesado, df_capacidades, zona, tipo_dia, tipo_vehiculo):

    if 'TIPO_VEHICULO_CALC' not in df_procesado.columns:
        df_procesado['TIPO_VEHICULO_CALC'] = df_procesado['PLACA'].apply(utils.clasificar_vehiculo_placa)
    
    df_f = df_procesado[(df_procesado['ZONA'] == zona) & (df_procesado['TIPO_DIA_CALC'] == tipo_dia) & (df_procesado['TIPO_VEHICULO_CALC'] == tipo_vehiculo)].copy()
   
    if len(df_f) == 0:
        return None
    
    fechas = df_f['DIA'].unique()
    horas = utils.obtener_rango_horas(df_f, tipo_dia)
    ocupacion_por_hora = {}
    entradas_por_hora = {}
    salidas_por_hora = {}

    for hora in horas:
        ocups, ents, sals = [], [], []
        for fecha in fechas:
            df_fecha = df_f[df_f['DIA'] == fecha]
            placas = set(df_fecha[df_fecha['HORA'] == hora]['PLACA'].dropna().unique())
            ocups.append(len(placas))
            
            if hora > min(horas):
                placas_ant = set(df_fecha[df_fecha['HORA'] == hora - 1]['PLACA'].dropna().unique())
                ents.append(len(placas - placas_ant))
                sals.append(len(placas_ant - placas))
            else:
                ents.append(len(placas))
                sals.append(0)

        ocupacion_por_hora[hora] = sum(ocups) if ocups else 0
        entradas_por_hora[hora] = sum(ents) if ents else 0
        salidas_por_hora[hora] = sum(sals) if sals else 0

    # Capacidad
    capacidad = 0
    if df_capacidades is not None:
        cap_zona = df_capacidades[df_capacidades['ZONA'] == zona]
        col = 'CAPACIDAD_AUTOS' if tipo_vehiculo == 'AUTO' else 'CAPACIDAD_MOTOS'
        capacidad = cap_zona[col].sum() if col in cap_zona.columns else 0
    
    # Indicadores
    ocup_max = max(ocupacion_por_hora.values()) if ocupacion_por_hora else 0
    ocup_media_pct = np.mean([o/capacidad*100 if capacidad > 0 else 0 for o in ocupacion_por_hora.values()])

    # Duración media (solo vehículos que entraron Y salieron durante el análisis)
    hora_min = min(horas)
    hora_max = max(horas)
    
    duraciones_data = []
    for fecha in fechas:
        df_fecha = df_f[df_f['DIA'] == fecha]
        for placa in df_fecha['PLACA'].unique():
            df_placa = df_fecha[df_fecha['PLACA'] == placa]
            horas_v = sorted(df_placa['HORA'].unique())
            if not horas_v:
                continue
            
            # Verificar que haya al menos 2 registros diferentes para calcular duración
            if len(df_placa) < 2 or len(horas_v) < 2:
                continue
            
            hora_entrada = min(horas_v)
            hora_salida = max(horas_v)
            
            # Solo contar si entró durante el análisis (no estaba antes) y salió durante el análisis (no está al final)
            entro_durante_analisis = hora_entrada >= hora_min
            salio_durante_analisis = hora_salida <= hora_max
            
            if entro_durante_analisis and salio_durante_analisis:
                # Usar HORA_COMPLETA (timestamp) para cálculo preciso
                timestamp_entrada = df_placa['HORA_COMPLETA'].min()
                timestamp_salida = df_placa['HORA_COMPLETA'].max()
                
                # Calcular duración en horas (con decimales)
                duracion = (timestamp_salida - timestamp_entrada).total_seconds() / 3600
                
                # Solo agregar si la duración es mayor a 0
                if duracion > 0:
                    duraciones_data.append({
                        'PLACA': placa,
                        'DIA': fecha,
                        'HORA_ENTRADA': timestamp_entrada,
                        'HORA_SALIDA': timestamp_salida,
                        'DURACION_HORAS': duracion
                    })
    
    # Crear DataFrame de duraciones
    df_duraciones = pd.DataFrame(duraciones_data) if duraciones_data else pd.DataFrame(columns=['PLACA', 'DIA', 'HORA_ENTRADA', 'HORA_SALIDA', 'DURACION_HORAS'])
    dur_media = df_duraciones['DURACION_HORAS'].mean() if len(df_duraciones) > 0 else 0
    
    # Convertir duración media a formato HH:MM
    horas_dur = int(dur_media)
    minutos_dur = int((dur_media - horas_dur) * 60)
    dur_media_formato = f"{horas_dur}:{minutos_dur:02d}"
    
    total_veh = df_f['PLACA'].nunique()
    total_ent = sum(entradas_por_hora.values())
    total_sal = sum(salidas_por_hora.values())

    irt = total_ent / capacidad if capacidad > 0 else 0
    irh = irt / len(horas) if horas else 0

    resultado = {
        'ocupacion_por_hora': ocupacion_por_hora,
        'entradas_por_hora': entradas_por_hora,
        'salidas_por_hora': salidas_por_hora,
        'capacidad': capacidad,
        'df_duraciones': df_duraciones,
        'indicadores': {
            'Ocupación Máxima': round(ocup_max, 0),
            'Demanda total': round(total_ent, 0),
            'Oferta Real Total': round(capacidad, 0),
            'Ocupación Media': f"{ocup_media_pct:.2f}%",
            'Duración Media (Dm)': dur_media_formato,
            'Índice de Rotación Total (IRt)': round(irt, 3),
            'Índice de Rotación Horario': round(irh, 3),
            'Tasa de Llegada': round(total_ent / capacidad if capacidad > 0 else 0, 1),
            'Tasa de Salida': round(total_sal / capacidad if capacidad > 0 else 0, 1),
            'Reserva de estacionamiento': round(capacidad - ocup_max, 0)
        },
        'total_vehiculos': total_veh,
        'n_fechas': len(fechas)
    }
    return resultado

def calcular_ocupacion_parqueadero(df_parqueaderos, zona, tipo_dia, tipo_vehiculo):
    if df_parqueaderos is None:
        return None
    
    df_f = df_parqueaderos[
    (df_parqueaderos['ZONA'] == zona) & 
    (df_parqueaderos['TIPO_DIA_CALC'] == tipo_dia) &
    (df_parqueaderos['TIPO_VEHICULO'] == tipo_vehiculo)
    ].copy()
    
    if len(df_f) == 0:
        return None
    
    fechas = df_f['DIA'].unique()
    # Obtener horas dinámicamente desde los datos reales
    horas = utils.obtener_rango_horas(df_f, tipo_dia)

    ocupacion_por_hora = {}
    entradas_por_hora = {}
    salidas_por_hora = {}

    for hora in horas:
        ocups, ents, sals = [], [], []
        for fecha in fechas:
            df_fecha = df_f[df_f['DIA'] == fecha]
            ent_acum = len(df_fecha[(df_fecha['TIPO_ENT_SAL'] == 'ENTRADA') & (df_fecha['HORA'] <= hora)])
            sal_acum = len(df_fecha[(df_fecha['TIPO_ENT_SAL'] == 'SALIDA') & (df_fecha['HORA'] <= hora)])
            ocups.append(max(0, ent_acum - sal_acum))
            
            ent_h = len(df_fecha[(df_fecha['TIPO_ENT_SAL'] == 'ENTRADA') & (df_fecha['HORA'] == hora)])
            sal_h = len(df_fecha[(df_fecha['TIPO_ENT_SAL'] == 'SALIDA') & (df_fecha['HORA'] == hora)])
            ents.append(ent_h)
            sals.append(sal_h)
        
        ocupacion_por_hora[hora] = sum(ocups) if ocups else 0
        entradas_por_hora[hora] = sum(ents) if ents else 0
        salidas_por_hora[hora] = sum(sals) if sals else 0
        
    # Capacidad
    capacidad = 0
    parqueaderos_unicos = [p for p in df_f['PARQUEADERO'].unique() if pd.notna(p)]
    for parq in parqueaderos_unicos:
        parq_df = df_f[df_f['PARQUEADERO'] == parq]
        if len(parq_df) == 0:
            continue
        parq_data = parq_df.iloc[0]
        col = 'CAPACIDAD_AUTOS' if tipo_vehiculo == 'AUTO' else 'CAPACIDAD_MOTOS'
        cap = parq_data.get(col, 0)
        if pd.notna(cap):
            try:
                capacidad += float(cap)
            except (ValueError, TypeError):
                pass
        
    return {
        'ocupacion_por_hora': ocupacion_por_hora,
        'entradas_por_hora': entradas_por_hora,
        'salidas_por_hora': salidas_por_hora,
        'capacidad': capacidad,
        'n_fechas': len(fechas)
    }
            
def generar_grafica_ocupacion(datos, zona, tipo_dia, tipo_vehiculo, tipo_est, filepath):

    horas = list(datos['ocupacion_por_hora'].keys())
    ocupacion = list(datos['ocupacion_por_hora'].values())

    # Crear gráfico de barras con Plotly
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=[f'{h}:00' for h in horas],
        y=ocupacion,
        marker_color=utils.COLORES['ocupacion'],
        marker_line_color='white',
        marker_line_width=1,
        text=[int(val) if val > 0 else '' for val in ocupacion],
        textposition='outside',
        textfont=dict(size=10)
    ))
    
    fig.update_layout(
        title=dict(
            text=f'Ocupación (Vehículos) - {zona}<br>{tipo_vehiculo}s - {tipo_dia} - {tipo_est}',
            font=dict(size=14, family='Arial, sans-serif'),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title='Hora',
        yaxis_title='Ocupación (Vehículos)',
        xaxis=dict(tickangle=-45),
        yaxis=dict(gridcolor='rgba(128,128,128,0.3)'),
        template='plotly_white',
        showlegend=False,
        height=600,
        width=1200
    )
    
    # Guardar siempre como HTML
    filepath_str = str(filepath)
    if not filepath_str.endswith('.html'):
        filepath_html = filepath_str.rsplit('.', 1)[0] + '.html'
    else:
        filepath_html = filepath_str
    fig.write_html(filepath_html)
