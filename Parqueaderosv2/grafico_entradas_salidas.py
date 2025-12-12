import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def calcular_entradas_salidas_hora(df_procesado):

    # Usar sets para placas únicas por hora
    placas_hora = df_procesado.groupby('HORA_GRUPO')['PLATE'].apply(set).to_dict()

    # Ordenar las horas
    horas_ordenadas = sorted(placas_hora.keys())
    entradas_salidas = []

    for i, hora in enumerate(horas_ordenadas):
        # Primera hora
        if i == 0:
            entradas = len(placas_hora[hora])
            salidas = 0
        else:
            hora_anterior = horas_ordenadas[i-1]
            # Entradas: revisa cuales placas son nuevas y las cuenta 
            entradas = len(placas_hora[hora] - placas_hora[hora_anterior])
            # Salidas: revisa cuales placas salieron y las cuenta 
            salidas = len(placas_hora[hora_anterior] - placas_hora[hora])
        
        entradas_salidas.append({'HORA': hora, 'ENTRADAS': entradas, 'SALIDAS': salidas})

    # Convertir la lista a DataFrame
    df_entradas_salidas_hora = pd.DataFrame(entradas_salidas)
    df_entradas_salidas_hora['HORA'] = df_entradas_salidas_hora['HORA'].astype(str).str.zfill(2) + ':00' #HH:00

    return df_entradas_salidas_hora

def generar_grafico_entradas_salidas(df_entradas_salidas, df_ocupacion):

    horas_labels = df_entradas_salidas['HORA']
    entradas_values = df_entradas_salidas['ENTRADAS']
    salidas_values = df_entradas_salidas['SALIDAS']
    ocupacion_values = df_ocupacion['OCUPACION']

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Barras azules para entradas 
    fig.add_trace(
        go.Bar(x=horas_labels, y=entradas_values, 
               name='Entradas', marker_color='blue', opacity=0.7),
        secondary_y=False
    )
    
    # Barras rojas para salidas
    fig.add_trace(
        go.Bar(x=horas_labels, y=salidas_values, 
               name='Salidas', marker_color='red', opacity=0.7),
        secondary_y=False
    )
    
    # Línea gris para ocupación
    fig.add_trace(
        go.Scatter(x=horas_labels, y=ocupacion_values,
                   name='Ocupación', mode='lines+markers',
                   line=dict(color='grey', width=3),
                   marker=dict(size=8)),
        secondary_y=False
    )
    
    # Configurar diseño
    fig.update_layout(
        title='Entradas y Salidas VS Ocupación de Vehículos',
        xaxis_title='Hora',
        barmode='group',  # Barras lado a lado
        template='plotly_white'
    )
    
    fig.show()
    return fig