

import pandas as pd
import geopandas as gpd
import json
import pyrosm
from shapely.ops import linemerge
import matplotlib.pyplot as plt
from contextily import add_basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import contextily as cx
import osmnx as ox




with open("proj4_params.json") as json_data:
    params = json.load(json_data)
gdf = gpd.read_file("proj4_points.geojson")



gdf.to_crs('epsg:2180', inplace=True)
buffered_points = gdf.copy()
buffered_points['geometry'] = buffered_points.buffer(100)




id_column = params["id_column"]



count_gdf= gpd.sjoin(gdf, buffered_points,predicate='intersects', how='right').groupby(id_column+'_right').size().reset_index(name='count')
count_gdf.rename(columns={id_column+'_right': id_column}, inplace=True)
count_gdf.to_csv("proj4_ex01_counts.csv",index=False)





gdf = gpd.read_file("proj4_points.geojson")
gdf.to_crs('epsg:4326', inplace=True)
gdf['lat'] = gdf['geometry'].y
gdf['lon'] = gdf['geometry'].x
gdf = gdf[[id_column,'lat', 'lon']]
gdf.to_csv("proj4_ex01_coords.csv",index=False)





city = params["city"]
fp = pyrosm.get_data(city)
osm = pyrosm.OSM(fp)
gdf_tertiary = osm.get_data_by_custom_criteria(custom_filter={'highway':['tertiary']})
gdf_tertiary = gdf_tertiary[gdf_tertiary['osm_type'] == 'way']



gdf_tertiary["geometry"] = gdf_tertiary["geometry"].apply(lambda geom: linemerge(geom) if geom.geom_type == "MultiLineString" else geom)
gdf_out = gpd.GeoDataFrame(gdf_tertiary[['id', 'name', 'geometry']], crs=gdf_tertiary.crs)
gdf_out.rename(columns={'id': 'osm_id'}, inplace=True)
gdf_out.to_file("proj4_ex02_roads.geojson", driver="GeoJSON", index=False)




roads = gpd.read_file("proj4_ex02_roads.geojson")
roads.to_crs('epsg:2180', inplace=True)
roads['buffer_geom'] = roads.geometry.buffer(50, cap_style=2, join_style=3)
roads = roads.set_geometry('buffer_geom')




lamps= gpd.read_file("proj4_points.geojson")
lamps.to_crs('epsg:2180', inplace=True)
lamps = lamps.set_geometry("geometry")




count_gdf= gpd.sjoin(roads,lamps, predicate='intersects', how='inner')
street_point_counts = count_gdf.groupby("name").size().reset_index(name='point_count')
street_point_counts





street_point_counts.to_csv("proj4_ex03_streets_points.csv",index=False)



countries_gdf = gpd.read_file("proj4_countries.geojson")
countries_gdf = gpd.GeoDataFrame(countries_gdf, geometry="geometry")


countries_gdf = gpd.read_file("proj4_countries.geojson")

countries_gdf['geometry'] = countries_gdf['geometry'].boundary

max_extent_x = countries_gdf.bounds['maxx'].max() - countries_gdf.bounds['minx'].min()
max_extent_y = countries_gdf.bounds['maxy'].max() - countries_gdf.bounds['miny'].min()
aspect_ratio = max_extent_y / max_extent_x

countries_gdf['geometry'] = countries_gdf['geometry'].scale(xfact=aspect_ratio+0.4, yfact=1, origin='center')

countries_gdf = countries_gdf.to_crs("EPSG:3857")


countries_gdf.to_pickle("proj4_ex04_gdf.pkl")

def render_country_boundary(country_name, gdf):
    country_boundary = gdf[gdf['name'] == country_name]
    if not country_boundary.empty:
        fig, ax = plt.subplots(figsize=(10, 10))
        country_boundary.plot(ax=ax, edgecolor='red', linewidth=1)
        add_basemap(ax, zoom=4, crs=country_boundary.crs) 
        filename = f"proj4_ex04_{country_name.lower().replace(' ', '_')}.png"
        plt.savefig(filename, bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
    else:
        print(f"Country '{country_name}' not found in the GeoDataFrame.")

for country_name in countries_gdf['name']:
    render_country_boundary(country_name, countries_gdf)






