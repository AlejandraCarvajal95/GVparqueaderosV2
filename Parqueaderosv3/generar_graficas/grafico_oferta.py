import plotly.graph_objects as go
import utils

def generar_grafica_oferta_ocupacion(datos, zona, tipo_dia, tipo_vehiculo, tipo_est, filepath):
    """Genera gráfica de ocupación vs capacidad."""

    horas = list(datos['ocupacion_por_hora'].keys())
    ocupacion = list(datos['ocupacion_por_hora'].values())
    capacidad = datos['capacidad']
    
    # Crear figura
    fig = go.Figure()
    
    # Línea de ocupación
    fig.add_trace(
        go.Scatter(
            x=[f'{h}:00' for h in horas],
            y=ocupacion,
            mode='lines+markers',
            name='Ocupación (Vehículos)',
            line=dict(color=utils.COLORES['ocupacion'], width=2),
            marker=dict(size=5)
        )
    )
    
    # Línea horizontal de oferta teórica
    fig.add_trace(
        go.Scatter(
            x=[f'{h}:00' for h in horas],
            y=[capacidad] * len(horas),
            mode='lines',
            name='Oferta Teórica Total',
            line=dict(color=utils.COLORES['oferta'], width=2)
        )
    )
    
    # Agregar líneas verticales entre ocupación y oferta (estética)
    shapes = []
    horas_labels = [f'{h}:00' for h in horas]
    for hora, o in zip(horas_labels, ocupacion):
        shapes.append(
            dict(
                type='line',
                x0=hora, x1=hora,
                y0=o, y1=capacidad,
                line=dict(color='grey', width=2, dash='dot')
            )
        )
    
    # Agregar áreas sombreadas donde ocupación > capacidad
    for i, o in enumerate(ocupacion):
        if o > capacidad:
            # Calcular las posiciones x para el rectángulo
            x0 = i - 0.5 if i > 0 else i
            x1 = i + 0.5 if i < len(horas) - 1 else i
            
            shapes.append(
                dict(
                    type='rect',
                    xref='x',
                    yref='y',
                    x0=x0,
                    x1=x1,
                    y0=capacidad,
                    y1=o,
                    fillcolor='red',
                    opacity=0.3,
                    line=dict(width=0)
                )
            )
    
    # Configurar diseño
    fig.update_layout(
        title=dict(
            text=f'Oferta vs Ocupación - {zona}<br>{tipo_vehiculo}s - {tipo_dia} - {tipo_est}',
            font=dict(size=12, family='Arial, sans-serif'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(text='Hora', font=dict(size=11)),
            tickangle=-45,
            type='category'  # Para que las shapes se alineen correctamente
        ),
        yaxis=dict(
            title=dict(text='Vehículos', font=dict(size=11)),
            rangemode='tozero'
        ),
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
        hovermode='x unified',
        shapes=shapes,
        showlegend=True
    )
    
    # Configurar grid
    fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
    
    # Guardar siempre como HTML
    filepath_str = str(filepath)
    if not filepath_str.endswith('.html'):
        filepath_html = filepath_str.rsplit('.', 1)[0] + '.html'
    else:
        filepath_html = filepath_str
    fig.write_html(filepath_html)

"""

def generar_grafico_oferta(df_oferta, df_ocupacion):

    # Calcular la suma total de ofertas teóricas
    oferta_teorica_total = df_oferta['oferta_teorica'].sum()
    horas_labels = df_ocupacion['HORA']
    ocupacion_values = df_ocupacion['OCUPACION']
   
    fig = go.Figure()
    
    # Línea de ocupación (azul)
    fig.add_trace(
        go.Scatter(x=horas_labels, y=ocupacion_values,
                   name='Ocupación (Vehículos)', mode='lines+markers',
                   line=dict(color='blue', width=3),
                   marker=dict(size=8))
    )
    
    # Línea constante de oferta teórica total (naranja)
    fig.add_trace(
        go.Scatter(x=horas_labels, y=[oferta_teorica_total]*len(horas_labels), 
                   name='Oferta Teórica Total', mode='lines',
                   line=dict(color='orange', width=3))
    )
    
    # Agregar líneas verticales entre oferta y ocupación
    shapes = []
    for i, (hora, ocupacion) in enumerate(zip(horas_labels, ocupacion_values)):
        shapes.append(
            dict(
                type='line',
                x0=hora, x1=hora,
                y0=ocupacion, y1=oferta_teorica_total,
                line=dict(color='grey', width=2, dash='dot')
            )
        )
    
    # Configurar diseño
    fig.update_layout(
        title='Oferta VS Ocupación',
        xaxis_title='Hora',
        template='plotly_white',
        shapes=shapes
    )
    
    fig.show()
    return fig

    
"""