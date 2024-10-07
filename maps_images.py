# Importar las librerías necesarias
import geopandas as gpd
import folium
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from rasterio.plot import show
from folium.plugins import HeatMap

import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
from shapely.geometry import Point

for i in range(1970,2019):
    # Cargar los datos de emisiones desde el archivo de texto
    file_path = f'/home/mazroj/Documents/JupyterNotebooks/hackathon_nasa/TOTALS_txt/v6.0_CH4_{i}_TOTALS.txt'  # Reemplaza con la ruta de tu archivo

    # Leer los datos (ajustar según el formato del archivo)
    data = pd.read_csv(file_path, sep=';', skiprows=3, names=['lat', 'lon', 'emission'])

    data['emission'] = np.where(data['emission'] > 2 *10**2, 1,0)
    data = data.loc[data['emission'] != 0]




    data['emission'] = np.log10(data['emission'])

    # Crear un GeoDataFrame con la geometría de puntos (lat, lon)
    geometry = [Point(xy) for xy in zip(data['lon'], data['lat'])]
    gdf = gpd.GeoDataFrame(data, geometry=geometry)

    # Filtrar los datos (esto es opcional si solo quieres una muestra)
    #gdf = gdf.sample(100000)

    # Crear el gráfico usando Cartopy
    fig = plt.figure(figsize=(15, 10))

    # Configurar el sistema de proyección (proyección de mapa Robinson para el mapa global)
    ax = plt.axes(projection=ccrs.Robinson())

    # Añadir características del mapa (costas, líneas de países)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    # Graficar las emisiones usando scatter plot
    sc = plt.scatter(
        gdf['lon'], gdf['lat'],  # Usar los datos del GeoDataFrame
        c=gdf['emission'],
        cmap='magma',  # Cambiar el esquema de colores si se desea
        s=0.0005,  # Tamaño de los puntos (ajustar según sea necesario)
        transform=ccrs.PlateCarree(),
        alpha=1
    )

    # Añadir barra de colores para la escala de emisiones
    cbar = plt.colorbar(sc, orientation='horizontal', pad=0.05)
    cbar.set_label('CH4 Tons/Year')

    # Título del gráfico
    plt.title(f'Global CH4 Emissions ({i})', fontsize=15)
    print(f'saving image {i}')
    # Mostrar el gráfico
    plt.savefig(f'/home/mazroj/Documents/JupyterNotebooks/hackathon_nasa/images/emissions_map_{i}.png',dpi = 300)
    print(f'Done image for {i}...')