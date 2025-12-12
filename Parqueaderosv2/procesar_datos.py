
from pathlib import Path
import pandas as pd
from grafico_entradas_salidas import calcular_entradas_salidas_hora, generar_grafico_entradas_salidas
from grafico_ocupacion import calcular_ocupacion_hora, generar_grafico_ocupacion
from grafico_oferta import generar_grafico_oferta
from grafico_zer import generar_grafico_zer

# PROCESAMIENTO DE DATOS
def procesar_estacionamientosDB():

    try:
     excel_path = Path('datos_entrada/Estacionamientos_BD.xls')
     df = pd.read_excel(excel_path)
    except Exception as e:
        print(f"Error al definir la ruta del archivo: {e}")
        return
    
    # Crear una copia 
    df_procesado = df[["FID", "PLATE", "TIMESTAMP", "CODIGO"]].copy()
    
    # Convertir TIMESTAMP a datetime y crear columnas DIA y HORA
    df_procesado['TIMESTAMP'] = pd.to_datetime(df_procesado['TIMESTAMP'])
    df_procesado['DIA'] = df_procesado['TIMESTAMP'].dt.date
    df_procesado['HORA'] = df_procesado['TIMESTAMP'].dt.strftime('%H:%M')
    
    # Reordenar columnas (mantener TIMESTAMP para cálculos)
    df_procesado = df_procesado[['FID', 'PLATE', 'DIA', 'HORA', 'TIMESTAMP', 'CODIGO']]
    
    return df_procesado

def procesar_ofertaDB():

    try:
        csv_path = Path('datos_entrada/oferta_temp.csv')
        df_oferta = pd.read_csv(csv_path) 
    except Exception as e:
        print(f"Error al definir la ruta del archivo: {e}")
        return
    
    df_oferta_procesado = df_oferta[['lado_manzana', 'oferta_teorica', 'zer']].copy()

    return df_oferta_procesado

if __name__ == "__main__":

    # Crear carpeta datos_salida si no existe
    output_dir = Path('datos_salida')
    output_dir.mkdir(exist_ok=True)

    df_procesado = procesar_estacionamientosDB()

     # Generar y guardar los gráficos como HTML

    # Gráfico de ocupación
    df_ocupacion = calcular_ocupacion_hora(df_procesado)
    grafico_ocupacion = generar_grafico_ocupacion(df_ocupacion)
    grafico_ocupacion.write_html(output_dir / 'grafico_ocupacion.html')

    # Gráfico de entradas y salidas
    df_entradas_salidas = calcular_entradas_salidas_hora(df_procesado)
    grafico_entradas_salidas = generar_grafico_entradas_salidas(df_entradas_salidas, df_ocupacion)
    grafico_entradas_salidas.write_html(output_dir / 'grafico_entradas_salidas.html')

    # Grafico de oferta teórica
    df_oferta_procesado= procesar_ofertaDB()
    
    grafico_oferta_teorica = generar_grafico_oferta(df_oferta_procesado, df_ocupacion)
    grafico_oferta_teorica.write_html(output_dir / 'grafico_oferta_teorica.html')

    # Grafico de oferta zer
    grafico_oferta_zer = generar_grafico_zer(df_oferta_procesado, df_ocupacion)
    grafico_oferta_zer.write_html(output_dir / 'grafico_oferta_zer.html')