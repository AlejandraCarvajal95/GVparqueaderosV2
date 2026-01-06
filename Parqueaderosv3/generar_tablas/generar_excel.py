from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime
from generar_tablas.escribir_datos import escribir_datos_ocupacion, escribir_indicadores, escribir_oferta_demanda
import utils

def generar_excel(zonas,df_autos,df_motos,df_parqueaderos, resultados, output_dir):
    """Genera archivo Excel con resultados."""
    wb = Workbook()
    
    header_fill = PatternFill(start_color=utils.COLORES['header'], end_color=utils.COLORES['header'], fill_type='solid')
    header_font = Font(bold=True, color=utils.COLORES['header_font'])
    border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    center = Alignment(horizontal='center', vertical='center')
    
    del wb['Sheet']
    
    # RESUMEN
    ws = wb.create_sheet('RESUMEN')
    ws['A1'] = 'ANÁLISIS DE ESTACIONAMIENTO'
    ws['A1'].font = Font(bold=True, size=14)
    ws['A3'] = f'Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M")}'
    ws['A4'] = f'Zonas: {", ".join(zonas)}'
    
    row = 6
    if df_autos is not None:
        ws[f'A{row}'] = f'Autos en vía: {len(df_autos):,} registros'
        row += 1
    if df_motos is not None:
        ws[f'A{row}'] = f'Motos en vía: {len(df_motos):,} registros'
        row += 1
    if df_parqueaderos is not None:
        ws[f'A{row}'] = f'Parqueaderos: {len(df_parqueaderos):,} registros'
    
    # INDICADORES VÍA - AUTOS
    if resultados['via']['autos']:
        ws = wb.create_sheet('IND_VIA_AUTOS')
        escribir_indicadores(ws, resultados['via']['autos'], 'INDICADORES - AUTOS EN VÍA', header_fill, header_font, border, center)
    
    # INDICADORES VÍA - MOTOS
    if resultados['via']['motos']:
        ws = wb.create_sheet('IND_VIA_MOTOS')
        escribir_indicadores(ws, resultados['via']['motos'], 'INDICADORES - MOTOS EN VÍA', header_fill, header_font, border, center)
    
    # TABLAS OFERTA/DEMANDA
    for zona, df_od in resultados['tablas_oferta_demanda'].items():
        nombre = f'OD_{utils.limpiar_nombre(zona)[:20]}'
        ws = wb.create_sheet(nombre)
        escribir_oferta_demanda(ws, df_od, zona, header_fill, header_font, border, center)
    
    # DATOS OCUPACIÓN
    ws = wb.create_sheet('DATOS_OCUPACION')
    escribir_datos_ocupacion(ws, header_fill, header_font, resultados)
    
    wb.save(output_dir / 'analisis_estacionamiento.xlsx')