import pandas as pd

def generar_tabla_oferta_demanda(zona, df_capacidades, df_autos, df_motos):
    """Genera tabla de oferta y demanda por lado de manzana."""
    if df_capacidades is None:
        return None
    
    cap_zona = df_capacidades[df_capacidades['ZONA'] == zona].copy()
    if len(cap_zona) == 0:
        return None
    
    resultados = []
    for _, row in cap_zona.iterrows():
        codigo = row['CODIGO_MANZANA']
        of_a = row.get('CAPACIDAD_AUTOS', 0)
        of_m = row.get('CAPACIDAD_MOTOS', 0)
        
        dem_a = {'TIPICO': 0, 'SABADO': 0, 'DOMINGO': 0}
        dem_m = {'TIPICO': 0, 'SABADO': 0, 'DOMINGO': 0}
        
        if df_autos is not None:
            for td in dem_a.keys():
                dem_a[td] = df_autos[(df_autos['CODIGO_MANZANA'] == codigo) & (df_autos['TIPO_DIA_CALC'] == td)]['PLACA'].nunique()
        
        if df_motos is not None:
            for td in dem_m.keys():
                dem_m[td] = df_motos[(df_motos['CODIGO_MANZANA'] == codigo) & (df_motos['TIPO_DIA_CALC'] == td)]['PLACA'].nunique()
        
        resultados.append({
            'LADOS': codigo,
            'OFERTA_AUTOS': of_a if pd.notna(of_a) else 0,
            'OFERTA_MOTOS': of_m if pd.notna(of_m) else 0,
            'AUTOS_TIPICO': dem_a['TIPICO'],
            'AUTOS_SABADO': dem_a['SABADO'],
            'AUTOS_DOMINGO': dem_a['DOMINGO'],
            'MOTOS_TIPICO': dem_m['TIPICO'],
            'MOTOS_SABADO': dem_m['SABADO'],
            'MOTOS_DOMINGO': dem_m['DOMINGO']
        })
    
    return pd.DataFrame(resultados)
