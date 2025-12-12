# Análisis de Estacionamientos

## Ejecución Rápida

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el proyecto
python procesar_datos.py
```

## Datos de Entrada

- `datos_entrada/Estacionamientos_BD.xls`: Datos de estacionamientos con FID, PLATE, TIMESTAMP y CODIGO
- `datos_entrada/oferta_temp.csv`: Datos de oferta con lado_manzana, oferta_teorica y zer

## Gráficos Generados

El proyecto genera 4 gráficos interactivos en formato HTML dentro de la carpeta `datos_salida/`:

1. **grafico_ocupacion.html**: Ocupación de estacionamientos por hora
2. **grafico_entradas_salidas.html**: Entradas y salidas de vehículos por hora
3. **grafico_oferta_teorica.html**: Comparación entre oferta teórica y ocupación
4. **grafico_oferta_zer.html**: Análisis de oferta con zonas especiales de regulación (ZER)
