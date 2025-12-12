import plotly.graph_objects as go

def generar_grafico_zer(df_oferta_procesado, df_ocupacion):

    # Calcular la suma total de ofertas teóricas
    oferta_zer_total = df_oferta_procesado['zer'].sum()
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
    
    # Línea constante de oferta teórica total (verde)
    fig.add_trace(
        go.Scatter(x=horas_labels, y=[oferta_zer_total]*len(horas_labels), 
                   name='Oferta Teórica Total', mode='lines',
                   line=dict(color='green', width=3))
    )
    
    # Agregar líneas verticales entre zer y ocupación
    shapes = []
    for i, (hora, ocupacion) in enumerate(zip(horas_labels, ocupacion_values)):
        shapes.append(
            dict(
                type='line',
                x0=hora, x1=hora,
                y0=ocupacion, y1=oferta_zer_total,
                line=dict(color='grey', width=2, dash='dot')
            )
        )
    
    # Configurar diseño
    fig.update_layout(
        title='Oferta VS ZER',
        xaxis_title='Hora',
        template='plotly_white',
        shapes=shapes
    )
    return fig