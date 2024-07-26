
import netCDF4 as nc
import numpy as np
def getPoint(pre, df, lat0, lon0, resolution, decimal=1):
    latIdx = ((lat0 - df["Lat"]) / resolution + 0.5).astype(np.int64)
    lonIdx = ((df["Lon"] - lon0) / resolution + 0.5).astype(np.int64)
    return pre[...,latIdx, lonIdx].round(decimals=decimal)
def Get_Lat_Lon_QPF(path,Lon_data,Lat_data):
    with nc.Dataset(path) as dataNC:
        latArr = dataNC["lat"][:]
        lonArr = dataNC["lon"][:]
        pre = dataNC["MQPF"][:] 
    data = getPoint(pre , {"Lon":Lon_data,"Lat":Lat_data} , latArr[0], lonArr[0], 0.01)
    return data
