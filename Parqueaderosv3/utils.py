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
    if len(placa) == 6 and placa[-1].isalpha():
        return 'MOTO'
    return 'AUTO'

def limpiar_nombre(nombre):
    """Limpia nombre para usar en archivos."""
    return nombre.replace(' ', '_').replace('(', '').replace(')', '').replace('/', '-')


HORAS_DIA_TIPICO = list(range(12, 18))  # 8:00 a 18:00
HORAS_DIA_ATIPICO = list(range(12, 18))  # 11:00 a 18:00

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
