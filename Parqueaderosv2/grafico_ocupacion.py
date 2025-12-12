import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

def calcular_ocupacion_hora(df_procesado):
    
    # Agrupar por HORA_GRUPO contando vehículos únicos (no registros repetidos)
    df_procesado['HORA_GRUPO'] = df_procesado['TIMESTAMP'].dt.hour
    ocupacion_hora = df_procesado.groupby('HORA_GRUPO')['PLATE'].nunique().reset_index(name='OCUPACION')
    ocupacion_hora['HORA'] = ocupacion_hora['HORA_GRUPO'].astype(str).str.zfill(2) + ':00' # HH:00
    
    # Ordenar por HORA_GRUPO y mostrar solo columnas relevantes
    ocupacion_hora = ocupacion_hora.sort_values(by='HORA_GRUPO')
    ocupacion_hora = ocupacion_hora[['HORA', 'OCUPACION']]

    return ocupacion_hora

def generar_grafico_ocupacion(df_ocupacion):

    horas_labels = df_ocupacion['HORA']
    ocupacion_values = df_ocupacion['OCUPACION']

    # Generar gráfico de barras
    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=horas_labels, y=ocupacion_values, 
               name='Ocupación', marker_color='steelblue', opacity=0.7)
    )
    
    # Diseño
    fig.update_layout(
        title='Ocupación (Vehiculos)',
        xaxis_title='Hora',
        yaxis_title='Ocupación (Vehículos)',
        template='plotly_white'
    )

    fig.show()
    return fig
