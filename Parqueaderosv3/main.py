from pathlib import Path
from generar_informe.generar_informe import generar_informe
from generar_tablas.tabla_oferta_ocupacion import generar_tabla_oferta_ocupacion
from generar_tablas.tabla_oferta_llegadas import generar_tabla_oferta_llegadas
from generar_tablas.tabla_oferta_irt import generar_tabla_oferta_irt
from generar_tablas.tabla_llegadas_oferta_ratio import generar_tabla_llegadas_oferta_ratio
import utils
from generar_graficas.grafico_entradas_salidas import generar_grafica_entradas_salidas
from generar_graficas.grafico_ocupacion import calcular_ocupacion_via, calcular_ocupacion_parqueadero, generar_grafica_ocupacion
from generar_graficas.grafico_oferta import generar_grafica_oferta_ocupacion
from procesar_datos import cargar_estacionamientosDB, cargar_capacidadesDB, procesar_autos, procesar_motos, procesar_parqueaderos, procesar_capacidadesDB, obtener_zonas_unicas
from generar_tablas.generar_excel import generar_excel

if __name__ == "__main__":

    # Crear carpeta datos_salida si no existe
    output_dir = Path('datos_salida')
    output_dir.mkdir(exist_ok=True)

    # cargar datos de estacionamientos y capacidades
    df_est_cargado = cargar_estacionamientosDB('datos_entrada/BD_10_12_25_estacionamiento.xlsx')
    df_capacidades_cargado = cargar_capacidadesDB('datos_entrada/20260103_BD_capacidades_v3.xlsx')

    # Procesar cada hoja de estacionamientos
    df_autos_procesado = procesar_autos(df_est_cargado[0])
    df_motos_procesado = procesar_motos(df_est_cargado[1])
    df_parqueaderos_procesado = procesar_parqueaderos(df_est_cargado[2])

  
    if df_autos_procesado is not None:
        # Agregar columna TIPO_VEHICULO_CALC para verificar, solo se usa para parqueaderos, no para vias
        df_autos_procesado['TIPO_VEHICULO_CALC'] = df_autos_procesado['PLACA'].apply(utils.clasificar_vehiculo_placa)

    if df_motos_procesado is not None:
        # Agregar columna TIPO_VEHICULO_CALC para verificar, solo se usa para parqueaderos, no para vias
        df_motos_procesado['TIPO_VEHICULO_CALC'] = df_motos_procesado['PLACA'].apply(utils.clasificar_vehiculo_placa)

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
        'tablas_oferta_ocupacion': {},
        'tablas_oferta_llegadas': {},
        'tablas_oferta_irt': {},
        'tablas_llegadas_oferta_ratio': {}
    }
   
    for zona in zonas:
        print(f"Procesando: {zona}")
        tiene_cap = df_capacidades_procesado is not None and len(df_capacidades_procesado[df_capacidades_procesado['ZONA'] == zona]) > 0
            
        # AUTOS en vía
        if df_autos_procesado is not None:
         
            for tipo_dia in tipos_dia:
                datos= calcular_ocupacion_via(df_autos_procesado, df_capacidades_procesado, zona, tipo_dia, 'AUTO')
                if datos:
                    #print ("datos autos:", datos)
                    key = f"{zona}_{tipo_dia}"
                    resultados['via']['autos'][key] = datos
                    base = f"VIA_AUTO_{utils.limpiar_nombre(zona)}_{tipo_dia}"
                    generar_grafica_ocupacion(datos, zona, tipo_dia, 'AUTO', 'En Vía', graficas_dir / f"{base}_ocupacion.png")
                    generar_grafica_entradas_salidas(datos, zona, tipo_dia, 'AUTO', 'En Vía', graficas_dir / f"{base}_entradas_salidas.png")
                    if tiene_cap and datos['capacidad'] > 0:
                        generar_grafica_oferta_ocupacion(datos, zona, tipo_dia, 'AUTO', 'En Vía', graficas_dir / f"{base}_oferta.png")
                  
        # MOTOS en vía
        if df_motos_procesado is not None:
            #print("--------------------MOTOS--------------------------------")
            for tipo_dia in tipos_dia:
                datos= calcular_ocupacion_via(df_motos_procesado, df_capacidades_procesado, zona, tipo_dia, 'MOTO')

                if datos:
                    key = f"{zona}_{tipo_dia}"
                    resultados['via']['motos'][key] = datos
                    base = f"VIA_MOTO_{utils.limpiar_nombre(zona)}_{tipo_dia}"
                    generar_grafica_ocupacion(datos, zona, tipo_dia, 'MOTO', 'En Vía', graficas_dir / f"{base}_ocupacion.png")
                    generar_grafica_entradas_salidas(datos, zona, tipo_dia, 'MOTO', 'En Vía', graficas_dir / f"{base}_entradas_salidas.png")
                    if tiene_cap and datos['capacidad'] > 0:
                        generar_grafica_oferta_ocupacion(datos, zona, tipo_dia, 'MOTO', 'En Vía', graficas_dir / f"{base}_oferta.png")
        
        # Tabla oferta/ocupacion
        if tiene_cap:
            tabla = generar_tabla_oferta_ocupacion(zona, df_capacidades_procesado, df_autos_procesado, df_motos_procesado)
            if tabla is not None:
                resultados['tablas_oferta_ocupacion'][zona] = tabla
        
        # Tabla oferta/llegadas
        if tiene_cap:
            tabla_lleg = generar_tabla_oferta_llegadas(zona, df_capacidades_procesado, df_autos_procesado, df_motos_procesado)
            if tabla_lleg is not None:
                resultados['tablas_oferta_llegadas'][zona] = tabla_lleg
        
        # Tabla oferta/IRT
        if tiene_cap:
            tabla_irt = generar_tabla_oferta_irt(zona, df_capacidades_procesado, df_autos_procesado, df_motos_procesado)
            if tabla_irt is not None:
                print("tabla_irt:", tabla_irt)
                print("//////////////////////////////")
                resultados['tablas_oferta_irt'][zona] = tabla_irt
            else:
                print("No se generó tabla IRT para zona:", zona)
        
        # Tabla llegadas/oferta ratio
        if tiene_cap:
            tabla_ratio = generar_tabla_llegadas_oferta_ratio(zona, df_capacidades_procesado, df_autos_procesado, df_motos_procesado)
            if tabla_ratio is not None:
                resultados['tablas_llegadas_oferta_ratio'][zona] = tabla_ratio
    
        # Parqueaderos Autos y Motos
        if df_parqueaderos_procesado is not None:
            for tipo_dia in tipos_dia:
                for tipo_veh in ['AUTO', 'MOTO']:
                    datos = calcular_ocupacion_parqueadero(df_parqueaderos_procesado, zona, tipo_dia, tipo_veh)
                    if datos and sum(datos['ocupacion_por_hora'].values()) > 0:
                        key = f"{zona}_{tipo_dia}"
                        tipo_key = 'autos' if tipo_veh == 'AUTO' else 'motos'
                        resultados['parqueadero'][tipo_key][key] = datos
                        
                        base = f"PARQ_{tipo_veh}_{utils.limpiar_nombre(zona)}_{tipo_dia}"
                        generar_grafica_ocupacion(datos, zona, tipo_dia, tipo_veh, 'Parqueadero', graficas_dir / f"{base}_ocupacion.png")
                        generar_grafica_entradas_salidas(datos, zona, tipo_dia, tipo_veh, 'Parqueadero', graficas_dir / f"{base}_entradas_salidas.png")
                        if datos['capacidad'] > 0:
                            generar_grafica_oferta_ocupacion(datos, zona, tipo_dia, tipo_veh, 'Parqueadero', graficas_dir / f"{base}_oferta.png")
    # Generar archivo Excel con resultados
    print(f"\nTablas IRT generadas: {list(resultados['tablas_oferta_irt'].keys())}")
    generar_excel(zonas,df_autos_procesado,df_motos_procesado,df_parqueaderos_procesado, resultados, output_dir)
    generar_informe(df_autos_procesado, df_motos_procesado, df_parqueaderos_procesado, zonas, resultados, output_dir, graficas_dir)
    print ("Análisis completado. Resultados guardados en 'datos_salida'.")