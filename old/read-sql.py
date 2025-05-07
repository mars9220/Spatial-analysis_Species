import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from shapely.geometry import Polygon
import sqlite3

# 連接 SQLite 資料庫
db_file = "/Users/jue-ying/Desktop/Data-Science-Class/GIS/物種多樣性/biology.sqlite"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()


# read database
print(pd.read_sql(f"""
SELECT grid_id,
       grid_minx,
       grid_miny,
       grid_maxx,
       grid_maxy,
       taxon_uuid,
       taxon_name_tw
  FROM 國內紅皮書名錄
  JOIN 哺乳類物種網格
    on 物種UUID = taxon_uuid
 Group BY 物種UUID         
                  """, conn))

# 關閉游標和連線
cursor.close()
conn.close()
