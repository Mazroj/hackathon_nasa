import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from shapely.geometry import Point
import pandas as pd

# Define fixed limits for color scale
vmin = 0  # Minimum value for emissions
vmax = 200  # Maximum value for emissions

# Define the geographical extent (optional, based on your data)
lon_min, lon_max = -180, 180
lat_min, lat_max = -60, 90  # Adjust as necessary for your data

for i in range(1970, 2019):
    # Cargar los datos de emisiones desde el archivo de texto
    file_path = f'/home/mazroj/Documents/JupyterNotebooks/hackathon_nasa/TOTALS_txt/v6.0_CH4_{i}_TOTALS.txt'

    # Leer los datos (ajustar según el formato del archivo)
    data = pd.read_csv(file_path, sep=';', skiprows=3, names=['lat', 'lon', 'emission'])

    # Filtrar las emisiones
    data['emission'] = np.where(data['emission'] > 2 * 10**2, 1, 0)
    data = data.loc[data['emission'] != 0]

    # Transformar las emisiones
    #data['emission'] = np.log10(data['emission'])

    # Crear un GeoDataFrame con la geometría de puntos (lat, lon)
    geometry = [Point(xy) for xy in zip(data['lon'], data['lat'])]
    gdf = gpd.GeoDataFrame(data, geometry=geometry)

    # Crear el gráfico usando Cartopy
    fig = plt.figure(figsize=(15, 10))

    # Configurar el sistema de proyección
    ax = plt.axes(projection=ccrs.Robinson())

    # Añadir características del mapa
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    # Establecer los límites del mapa
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

    # Graficar las emisiones usando scatter plot
    sc = plt.scatter(
        gdf['lon'], gdf['lat'],
        c=gdf['emission'],
        cmap='magma',
        s=0.0005,
        transform=ccrs.PlateCarree(),
        alpha=1
    )

    # Establecer límites de color
    sc.set_clim(vmin=vmin, vmax=vmax)

    # Añadir barra de colores para la escala de emisiones
    cbar = plt.colorbar(sc, orientation='horizontal', pad=0.05)
    cbar.set_label('CH4 Tons/Year')

    # Título del gráfico
    plt.title(f'Global CH4 Emissions ({i})', fontsize=15)

    # Guardar la imagen
    plt.savefig(f'/home/mazroj/Documents/JupyterNotebooks/hackathon_nasa/images/emissions_map_{i}.png', dpi=300)
    plt.close()  # Cerrar la figura para evitar la sobrecarga de memoria
    print(f'Done image for {i}...')
