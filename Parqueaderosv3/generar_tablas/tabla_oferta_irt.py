import pandas as pd
import utils

def generar_tabla_oferta_irt(zona, df_capacidades, df_autos, df_motos):
    """Genera tabla de oferta e índice de rotación total (IRT) por lado de manzana."""
    if df_capacidades is None:
        return None
    
    cap_zona = df_capacidades[df_capacidades['ZONA'] == zona].copy()
    if len(cap_zona) == 0:
        return None
    
    resultados = []
    for _, row in cap_zona.iterrows():
        codigo = row['CODIGO_MANZANA']
        of_a = row.get('CAPACIDAD_AUTOS', 0) if pd.notna(row.get('CAPACIDAD_AUTOS', 0)) else 0
        of_m = row.get('CAPACIDAD_MOTOS', 0) if pd.notna(row.get('CAPACIDAD_MOTOS', 0)) else 0
        
        irt_a = {'TIPICO': 0, 'SABADO': 0, 'DOMINGO': 0}
        irt_m = {'TIPICO': 0, 'SABADO': 0, 'DOMINGO': 0}
        
        # Calcular IRT para AUTOS
        if df_autos is not None:
            for td in irt_a.keys():
                entradas_totales = calcular_entradas_totales(df_autos, codigo, td)
                irt_a[td] = round(entradas_totales / of_a, 3) if of_a > 0 else 0
        
        # Calcular IRT para MOTOS
        if df_motos is not None:
            for td in irt_m.keys():
                entradas_totales = calcular_entradas_totales(df_motos, codigo, td)
                irt_m[td] = round(entradas_totales / of_m, 3) if of_m > 0 else 0
        
        resultados.append({
            'LADOS': codigo,
            'OFERTA_AUTOS': of_a,
            'OFERTA_MOTOS': of_m,
            'IRT_AUTOS_TIPICO': irt_a['TIPICO'],
            'IRT_AUTOS_SABADO': irt_a['SABADO'],
            'IRT_AUTOS_DOMINGO': irt_a['DOMINGO'],
            'IRT_MOTOS_TIPICO': irt_m['TIPICO'],
            'IRT_MOTOS_SABADO': irt_m['SABADO'],
            'IRT_MOTOS_DOMINGO': irt_m['DOMINGO']
        })
    
    return pd.DataFrame(resultados)

def calcular_entradas_totales(df, codigo_manzana, tipo_dia):
    """Calcula el total de entradas para una manzana y tipo de día específico."""
    df_filtrado = df[(df['CODIGO_MANZANA'] == codigo_manzana) & (df['TIPO_DIA_CALC'] == tipo_dia)]
    
    if len(df_filtrado) == 0:
        return 0
    
    # Obtener fechas únicas
    fechas = df_filtrado['DIA'].unique()
    # Obtener horas dinámicamente desde los datos reales
    horas = utils.obtener_rango_horas(df_filtrado, tipo_dia)
    
    entradas_por_hora = {}
    for hora in horas:
        ents = []
        for fecha in fechas:
            df_fecha = df_filtrado[df_filtrado['DIA'] == fecha]
            placas = set(df_fecha[df_fecha['HORA'] == hora]['PLACA'].dropna().unique())
            
            if hora > min(horas):
                placas_ant = set(df_fecha[df_fecha['HORA'] == hora - 1]['PLACA'].dropna().unique())
                ents.append(len(placas - placas_ant))
            else:
                ents.append(len(placas))
        
        entradas_por_hora[hora] = sum(ents) / len(fechas) if len(fechas) > 0 else 0
    
    return sum(entradas_por_hora.values())

