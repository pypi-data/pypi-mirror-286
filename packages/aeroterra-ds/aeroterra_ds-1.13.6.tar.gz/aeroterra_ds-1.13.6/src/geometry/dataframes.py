import os

from enum import Enum

import geopandas as gpd
import pandas as pd

from geometry.change_crs import change_box_crs, change_crs
from geometry.checks import is_bbox, is_polygon_like, is_multi_geometry, is_geometry

from shapely.geometry import Polygon, MultiPolygon, box

class GDFSaveTypes(Enum):
    SHAPEFILE = 0
    GDB = 1

class DateSaveTypes(Enum):
    ISOFORMAT = 0
    TIMESTAMP = 1


def concat_geopandas(dataframes_to_join, crs=None, geometry_column="geometry"):
    """
    Concatenate geodataframes keeping the geodataframe format

    Parameters:
        - dataframes_to_join: List of dataframes to join.
        - crs (Optional): CRS to save the result in. If None, the one
            of the first dataframe will be used.
        - geometry_column (Optional): Name of the column where the geometry should be saved.
            By default "geometry" will be assumed
    """
    actual_gdfs = []
    for gdf in dataframes_to_join:
        if gdf is None:
            continue
        if not isinstance(gdf, gpd.GeoDataFrame):
            raise Exception("Must Concatenate All GeoDataFrames")
        
        if gdf.crs is None:
            raise Exception("Can't Concatenate GeoDataFrames Without an assigned CRS")
        if gdf.geometry is None:
            raise Exception("Can't Concatenate GeoDataFrames Without an assigned Geometry Column")
        actual_gdfs.append(gdf)

    if len(actual_gdfs) == 0:
        raise Exception("Must Concatenate At Least 1 GeoDataFrame")
    
    if crs is None:
        crs = actual_gdfs[0].crs
    
    for gdf in actual_gdfs:
        gdf.to_crs(crs, inplace=True)
        geom_column = gdf.geometry.name
        if geom_column != geometry_column:
            gdf.rename(columns={geom_column: geometry_column}, inplace=True)
    
    total = pd.concat(actual_gdfs)

    return gpd.GeoDataFrame(total, crs=crs, geometry=geometry_column)


def create_gdf_geometries(geometries, crs, split_multi=False, geometry_column="geometry"):
    """
    Given a group of geometries it creates a geodataframe with them.

    Parameters:
        - geometries: Geometries/Geometry to create a GDF for
        - crs: CRS of the given geometries
        - split_multi (Optional): If it should split the multigeometries into
            its separated parts. By default in False.
        - geometry_column (Optional): What name to give the geoemtry column.
            By default set in 'geometry'
    """
    if isinstance(geometries, gpd.GeoDataFrame):
        response = geometries.copy()
    elif isinstance(geometries, gpd.GeoSeries):
        response = gpd.GeoDataFrame({geometry_column: geometries}, geometry=geometry_column, crs=crs)
    elif is_bbox(geometries):
        pol = box(geometries)
        response = gpd.GeoDataFrame({geometry_column: [pol]}, geometry=geometry_column, crs=crs)
    elif is_multi_geometry(geometries) and split_multi:
        geometries = list(geometries.geoms)
        response = gpd.GeoDataFrame({geometry_column: geometries}, geometry=geometry_column, crs=crs)
    elif is_geometry(geometries):
        response = gpd.GeoDataFrame({geometry_column: [geometries]}, geometry=geometry_column, crs=crs)
    elif isinstance(geometries, list):
        if len(geometries) == 0:
            raise Exception("Can't Filter To An Empty List")
        if not is_geometry(geometries[0]):
            raise Exception("Can't Create A GDF from NOT Geometries")
        if is_multi_geometry(geometries) and split_multi:
            geometries = [geometry.geoms for geometry in geometries]

        response = gpd.GeoDataFrame({geometry_column: geometries}, geometry=geometry_column, crs=crs)
    
    geom_column = response.geometry.name
    if geom_column != geometry_column:
        response.rename(columns={geom_column: geometry_column}, inplace=True)

    return response.to_crs(crs)


def check_gdf_path(path, driver):
    """
    Check if a given path and driver type is a valid path to save a GDF

    Parameters:
        - path: Path to check
        - driver: Driver of the wanted path. A type of the GDFSaveTypes Enum
    """
    _base_name, extension = os.path.splitext(path)
    if driver == GDFSaveTypes.SHAPEFILE:
        is_folder = len(extension) == 0
        is_shp = extension == ".shp"

        if not is_folder and not is_shp:
            raise Exception("Invalid Path, Must Provide A Folder Or A Shapefile Path")
    elif driver == GDFSaveTypes.GDB:
        is_gdb = extension == ".gdb"

        if not is_gdb:
            raise Exception("Invalid Path, Must Provide A GDB Path")
    else:
        raise Exception("Invalid Driver")


def save_gdf(gdf, path, driver=GDFSaveTypes.SHAPEFILE, date_to=DateSaveTypes.ISOFORMAT, gdb_layer=None):
    """
    Given a group of geometries it creates a geodataframe with them.

    Parameters:
        - gdf: GeoDataFrame to save
        - path: Path where to save the gdf
        - driver (Optional): How to save the GDF, a type of the
            GDFSaveTypes Enum. By Default in Shapefile
        - date_to (Optional): How to save a datetime type, a type of
            the DateSaveTypes Enum. By default in Isoformat
        - gdb_layer (Optional): Layer name where to save if stored
            in a GDB
    """
    if not isinstance(gdf, gpd.GeoDataFrame):
        raise Exception("Invalid GDF")

    check_gdf_path(path, driver)

    parsed_gdf = gdf.copy()
    gdf_types = dict(parsed_gdf.dtypes)

    for column, data_type in gdf_types.items():
        str_type = str(data_type).lower()
        if str_type.find("float") >= 0:
            parsed_gdf[column] = parsed_gdf[column].astype(float)
            continue
        
        if str_type.find("int") >= 0:
            parsed_gdf[column] = parsed_gdf[column].astype(int)
            continue
        
        if str_type.find("datetime") >= 0 and driver == GDFSaveTypes.SHAPEFILE:
            if date_to == DateSaveTypes.ISOFORMAT:
                parsed_gdf[column] = parsed_gdf[column].apply(lambda s: s.isoformat())
            elif date_to == DateSaveTypes.TIMESTAMP:
                parsed_gdf[column] = parsed_gdf[column].apply(lambda s: s.timestamp()).astype(float)
            continue
    
    if driver == GDFSaveTypes.SHAPEFILE:
        parsed_gdf.to_file(path)
    elif driver == GDFSaveTypes.GDB:
        parsed_gdf.to_file(path, driver="OpenFileGDB", layer=gdb_layer)