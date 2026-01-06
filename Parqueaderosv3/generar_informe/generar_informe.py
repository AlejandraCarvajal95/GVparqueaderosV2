from datetime import datetime
\

def generar_informe(df_autos, df_motos, df_parqueaderos, zonas, resultados, output_dir, graficas_dir):
    """Genera informe técnico."""
    inf = []
    inf.append("=" * 80)
    inf.append("INFORME TÉCNICO - ANÁLISIS DE ESTACIONAMIENTO")
    inf.append(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    inf.append("=" * 80)
    
    inf.append("\n1. DATOS DE ENTRADA")
    inf.append("-" * 40)
    
    if df_autos is not None:
        inf.append(f"   Autos en vía: {len(df_autos):,} registros, {df_autos['PLACA'].nunique():,} placas únicas")
    if df_motos is not None:
        inf.append(f"   Motos en vía: {len(df_motos):,} registros, {df_motos['PLACA'].nunique():,} placas únicas")
    if df_parqueaderos is not None:
        inf.append(f"   Parqueaderos: {len(df_parqueaderos):,} movimientos")
    
    inf.append(f"\n   Zonas: {', '.join(zonas)}")
    
    inf.append("\n2. METODOLOGÍA")
    inf.append("-" * 40)
    inf.append("   - Ocupación: Conteo de vehículos únicos por hora")
    inf.append("   - Entradas: Vehículos nuevos vs hora anterior")
    inf.append("   - Salidas: Vehículos que no continúan")
    inf.append("   - Valores promediados por tipo de día")
    inf.append("   - Típico: Lun-Vie (8-18h), Atípico: Sáb-Dom (11-18h)")
    
    inf.append("\n3. RESULTADOS POR ZONA")
    inf.append("-" * 40)
    
    for zona in zonas:
        inf.append(f"\n>>> {zona}")
        for tipo_dia in ['TIPICO', 'SABADO', 'DOMINGO']:
            key = f"{zona}_{tipo_dia}"
            if key in resultados['via']['autos']:
                d = resultados['via']['autos'][key]
                inf.append(f"\n   AUTOS - {tipo_dia}:")
                for i, v in d['indicadores'].items():
                    inf.append(f"      {i}: {v}")
    
    inf.append("\n4. ARCHIVOS GENERADOS")
    inf.append("-" * 40)
    inf.append(f"   - Excel: analisis_estacionamiento.xlsx")
    inf.append(f"   - Gráficas: {len(list(graficas_dir.glob('*.html')))} archivos HTML")
    
    inf.append("\n5. OBSERVACIONES")
    inf.append("-" * 40)
    
    saturadas = []
    for key, d in resultados['via']['autos'].items():
        if 'indicadores' in d:
            r = d['indicadores'].get('Reserva de estacionamiento', 0)
            if isinstance(r, (int, float)) and r < 0:
                zona, td = key.rsplit('_', 1)
                saturadas.append(f"{zona} ({td}): déficit {abs(r):.0f}")
    
    if saturadas:
        inf.append("   Zonas con saturación:")
        for s in saturadas:
            inf.append(f"   - {s}")
    else:
        inf.append("   No se detectó saturación crítica.")
    
    inf.append("\n" + "=" * 80)
    
    with open(output_dir / 'informe_tecnico.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(inf))

