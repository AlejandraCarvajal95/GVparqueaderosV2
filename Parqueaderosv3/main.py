from pathlib import Path
import utils
from generar_graficas.grafico_entradas_salidas import generar_grafica_entradas_salidas
from generar_graficas.grafico_ocupacion import calcular_ocupacion_via, generar_grafica_ocupacion
from generar_graficas.grafico_oferta import generar_grafica_oferta_ocupacion
from procesar_datos import cargar_estacionamientosDB, cargar_capacidadesDB, procesar_autos, procesar_motos, procesar_parqueaderos, procesar_capacidadesDB, obtener_zonas_unicas


if __name__ == "__main__":

    # Crear carpeta datos_salida si no existe
    output_dir = Path('datos_salida')
    output_dir.mkdir(exist_ok=True)

    # cargar datos de estacionamientos y capacidades
    df_est_cargado = cargar_estacionamientosDB()
    df_capacidades_cargado = cargar_capacidadesDB()

    # Procesar cada hoja de estacionamientos
    df_autos_procesado = procesar_autos(df_est_cargado[0])
    df_motos_procesado = procesar_motos(df_est_cargado[1])
    df_parqueaderos_procesado = procesar_parqueaderos(df_est_cargado[2])

    # Procesar datos de capacidades
    df_capacidades_procesado = procesar_capacidadesDB(df_capacidades_cargado)

    # Obtener listas únicas para análisis posteriores
    tipos_dia = ["TIPICO", "SABADO", "DOMINGO"]
    zonas = obtener_zonas_unicas(df_autos_procesado, df_motos_procesado, df_capacidades_procesado)

    output_dir = Path(output_dir)
    graficas_dir = output_dir / 'graficas'
    graficas_dir.mkdir(parents=True, exist_ok=True)

    resultados = {
        'via': {'autos': {}, 'motos': {}},
        'parqueadero': {'autos': {}, 'motos': {}},
        'tablas_oferta_demanda': {}
    }

    for zona in zonas:
        print(f"Procesando: {zona}")
        tiene_cap = df_capacidades_procesado is not None and len(df_capacidades_procesado[df_capacidades_procesado['ZONA'] == zona]) > 0
            
        # AUTOS en vía
        if df_autos_procesado is not None:
            for tipo_dia in tipos_dia:
                datos = calcular_ocupacion_via(df_autos_procesado, df_capacidades_procesado, zona, tipo_dia, 'AUTO')
                if datos:
                    key = f"{zona}_{tipo_dia}"
                    resultados['via']['autos'][key] = datos
                    base = f"VIA_AUTO_{utils.limpiar_nombre(zona)}_{tipo_dia}"
                    generar_grafica_ocupacion(datos, zona, tipo_dia, 'AUTO', 'En Vía', graficas_dir / f"{base}_ocupacion.png")
                    generar_grafica_entradas_salidas(datos, zona, tipo_dia, 'AUTO', 'En Vía', graficas_dir / f"{base}_entradas_salidas.png")
                    if tiene_cap and datos['capacidad'] > 0:
                        generar_grafica_oferta_ocupacion(datos, zona, tipo_dia, 'AUTO', 'En Vía', graficas_dir / f"{base}_oferta.png")
                  
        # MOTOS en vía
        if df_motos_procesado is not None:
            for tipo_dia in tipos_dia:
                datos = calcular_ocupacion_via(df_motos_procesado, df_capacidades_procesado, zona, tipo_dia, 'MOTO')
                if datos:
                    key = f"{zona}_{tipo_dia}"
                    resultados['via']['motos'][key] = datos
                    base = f"VIA_MOTO_{utils.limpiar_nombre(zona)}_{tipo_dia}"
                    generar_grafica_ocupacion(datos, zona, tipo_dia, 'MOTO', 'En Vía', graficas_dir / f"{base}_ocupacion.png")
                    generar_grafica_entradas_salidas(datos, zona, tipo_dia, 'MOTO', 'En Vía', graficas_dir / f"{base}_entradas_salidas.png")
   



    # Generar y guardar los gráficos como HTML

    # Gráfico de ocupación
    #df_ocupacion = calcular_ocupacion_hora(df_procesado)
    #grafico_ocupacion = generar_grafico_ocupacion(df_ocupacion)
    #grafico_ocupacion.write_html(output_dir / 'grafico_ocupacion.html')

    # Gráfico de entradas y salidas
    #df_entradas_salidas = calcular_entradas_salidas_hora(df_procesado)
    #grafico_entradas_salidas = generar_grafico_entradas_salidas(df_entradas_salidas, df_ocupacion)
    #grafico_entradas_salidas.write_html(output_dir / 'grafico_entradas_salidas.html')

    # Grafico de oferta teórica
    #df_oferta_procesado= cargar_capacidadesDB()
    
    #grafico_oferta_teorica = generar_grafico_oferta(df_oferta_procesado, df_ocupacion)
    #grafico_oferta_teorica.write_html(output_dir / 'grafico_oferta_teorica.html')

   
   