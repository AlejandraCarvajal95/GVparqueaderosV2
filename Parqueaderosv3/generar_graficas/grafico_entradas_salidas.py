import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import utils

def generar_grafica_entradas_salidas(datos, zona, tipo_dia, tipo_vehiculo, tipo_est, filepath):

    horas = list(datos['ocupacion_por_hora'].keys())
    ocupacion = list(datos['ocupacion_por_hora'].values())
    entradas = list(datos['entradas_por_hora'].values())
    salidas = list(datos['salidas_por_hora'].values())
    
    # Crear figura con eje secundario (equivalente a twinx)
    fig = make_subplots(specs=[[{"secondary_y": False}]])
    
    # Barras de entradas (equivalente a ax.bar con offset negativo)
    fig.add_trace(
        go.Bar(
            x=[f'{h}:00' for h in horas],
            y=entradas,
            name='Llegan',
            marker_color=utils.COLORES['entradas'],
            offsetgroup=0
        ),
        secondary_y=False
    )
    
    # Barras de salidas (equivalente a ax.bar con offset positivo)
    fig.add_trace(
        go.Bar(
            x=[f'{h}:00' for h in horas],
            y=salidas,
            name='Salen',
            marker_color=utils.COLORES['salidas'],
            offsetgroup=1
        ),
        secondary_y=False
    )
    
    # Línea de ocupación en eje secundario (equivalente a ax2.plot)
    fig.add_trace(
        go.Scatter(
            x=[f'{h}:00' for h in horas],
            y=ocupacion,
            name='Ocupación',
            mode='lines+markers',
            line=dict(color=utils.COLORES['linea_ocupacion'], width=2),
            marker=dict(size=4)
        ),
        secondary_y=False
    )
    
    # Configurar diseño
    fig.update_layout(
        title=dict(
            text=f'Entradas y Salidas vs Ocupación - {zona}<br>{tipo_vehiculo}s - {tipo_dia} - {tipo_est}',
            font=dict(size=12, family='Arial, sans-serif'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(text='Hora', font=dict(size=11)),
            tickangle=-45
        ),
        barmode='group',
        width=1200,
        height=600,
        template='plotly_white',
        legend=dict(
            x=0.01,
            y=0.99,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(255,255,255,0.8)'
        ),
        hovermode='x unified'
    )
    
    # Configurar títulos de ejes Y
    fig.update_yaxes(
        title_text='Entradas / Salidas',
        title_font=dict(size=11),
        secondary_y=False,
        showgrid=True,
        gridcolor='rgba(0,0,0,0.1)'
    )
    
    fig.update_yaxes(
        title_text='Ocupación (Vehículos)',
        title_font=dict(size=11),
        secondary_y=True
    )
    
    # Guardar siempre como HTML
    filepath_str = str(filepath)
    if not filepath_str.endswith('.html'):
        filepath_html = filepath_str.rsplit('.', 1)[0] + '.html'
    else:
        filepath_html = filepath_str
    fig.write_html(filepath_html)

