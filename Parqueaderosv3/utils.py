import pandas as pd

def clasificar_dia(dia_semana):
    """Clasifica el día: TIPICO (Lun-Vie), SABADO, DOMINGO."""
    if dia_semana < 5:
        return 'TIPICO'
    elif dia_semana == 5:
        return 'SABADO'
    return 'DOMINGO'
    
def clasificar_vehiculo_placa(placa):
    """Clasifica tipo de vehículo por formato de placa colombiana."""
    if pd.isna(placa):
        return 'DESCONOCIDO'
    placa = str(placa).upper().strip()
    # Limpiar caracteres no alfanuméricos (puntos, espacios extra, etc.)
    placa = ''.join(c for c in placa if c.isalnum())
    if len(placa) == 6 and placa[-1].isalpha():
        return 'MOTO'
    return 'AUTO'

def limpiar_nombre(nombre):
    """Limpia nombre para usar en archivos."""
    return nombre.replace(' ', '_').replace('(', '').replace(')', '').replace('/', '-')

def obtener_rango_horas(df, tipo_dia, hora_final=18):
    """
    Obtiene el rango de horas a procesar basado en los datos reales.
    
    Args:
        df: DataFrame con columna HORA y TIPO_DIA_CALC
        tipo_dia: 'TIPICO', 'SABADO', o 'DOMINGO'
        hora_final: Hora máxima (límite superior), default 18
    
    Returns:
        list: Rango de horas a procesar
    """
    if df is None or len(df) == 0:
        # Valores por defecto si no hay datos
        return list(range(12, hora_final))
    
    df_filtrado = df[df['TIPO_DIA_CALC'] == tipo_dia]
    
    if len(df_filtrado) == 0:
        # Si no hay datos para ese tipo de día, usar rango por defecto
        return list(range(12, hora_final))
    
    # Obtener hora mínima de los datos reales
    hora_min = int(df_filtrado['HORA'].min())
    
    # Generar rango desde hora_min hasta hora_final (sin incluir hora_final)
    return list(range(hora_min, hora_final))

# Mantener constantes para referencia (ya no se usan directamente)
#HORAS_DIA_TIPICO = list(range(12, 18))  # Recordatorio: datos desde ~8:00
#HORAS_DIA_ATIPICO = list(range(12, 18))  # Recordatorio: datos desde ~11:00

COLORES = {
    'ocupacion': '#4472C4',
    'entradas': '#4472C4', 
    'salidas': '#C55A5A',
    'linea_ocupacion': '#7F7F7F',
    'oferta': '#ED7D31',
    'header': 'FF4472C4',
    'header_font': 'FFFFFFFF',
    'alt_row': 'FFE6F0FF'
}
