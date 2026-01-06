import pandas as pd

def generar_tabla_llegadas_oferta_ratio(zona, df_capacidades, df_autos, df_motos):
    """Genera tabla con ratio de llegadas totales / oferta por lado de manzana."""
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
        
        ratio_a = {'TIPICO': 0, 'SABADO': 0, 'DOMINGO': 0}
        ratio_m = {'TIPICO': 0, 'SABADO': 0, 'DOMINGO': 0}
        
        # Calcular ratio para AUTOS
        if df_autos is not None:
            for td in ratio_a.keys():
                # Contar registros totales (llegadas)
                llegadas = len(df_autos[(df_autos['CODIGO_MANZANA'] == codigo) & (df_autos['TIPO_DIA_CALC'] == td)])
                # Calcular ratio = Llegadas / Oferta
                ratio_a[td] = round(llegadas / of_a, 3) if of_a > 0 else 0
        
        # Calcular ratio para MOTOS
        if df_motos is not None:
            for td in ratio_m.keys():
                # Contar registros totales (llegadas)
                llegadas = len(df_motos[(df_motos['CODIGO_MANZANA'] == codigo) & (df_motos['TIPO_DIA_CALC'] == td)])
                # Calcular ratio = Llegadas / Oferta
                ratio_m[td] = round(llegadas / of_m, 3) if of_m > 0 else 0
        
        resultados.append({
            'LADOS': codigo,
            'OFERTA_AUTOS': of_a,
            'OFERTA_MOTOS': of_m,
            'LLEGADAS_OFERTA_AUTOS_TIPICO': ratio_a['TIPICO'],
            'LLEGADAS_OFERTA_AUTOS_SABADO': ratio_a['SABADO'],
            'LLEGADAS_OFERTA_AUTOS_DOMINGO': ratio_a['DOMINGO'],
            'LLEGADAS_OFERTA_MOTOS_TIPICO': ratio_m['TIPICO'],
            'LLEGADAS_OFERTA_MOTOS_SABADO': ratio_m['SABADO'],
            'LLEGADAS_OFERTA_MOTOS_DOMINGO': ratio_m['DOMINGO']
        })
    
    return pd.DataFrame(resultados)
