import matplotlib.colors as mcolors
import seaborn as sns
import jenkspy
import numpy as np
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import sqlite3
import json

from matplotlib.colors import Normalize
from matplotlib.cm import viridis

db_file = "/Users/jue-ying/Desktop/Data-Science-Class/GIS/物種多樣性/biology-all.sqlite"
conn = sqlite3.connect(db_file)

# 從 JSON 檔案讀取表格名稱
with open("tables.json", "r") as file:
    data = json.load(file)
    table_names = data["table_names"]

all_counts = []  # 用於儲存所有計數的列表

for table_name in table_names:
    sql_query = f"""
        SELECT
            grid_id,
            grid_minx,
            grid_miny,
            grid_maxx,
            grid_maxy,
            COUNT(*) AS count
        FROM {table_name}
        JOIN 國內紅皮書名錄 on 物種UUID = taxon_uuid
        WHERE 國內紅皮書評估類別 IN ('易危（VU, Vulnerable）', '瀕危（EN, Endangered）','極危（CR, Critically Endangered）')
        GROUP BY grid_minx, grid_miny, grid_maxx, grid_maxy
    """
    df = pd.read_sql(sql_query, conn)
    all_counts.append(df)

# 合併所有計數
all_counts = [df for df in all_counts if not df.empty]  # Exclude empty DataFrames
combined_df = pd.concat(all_counts, ignore_index=True)
# 聚合計數
final_df = combined_df.groupby(["grid_id","grid_minx", "grid_miny", "grid_maxx", "grid_maxy"])[
    "count"].sum().reset_index()

final_df.rename(columns={"grid_minx": "minx", "grid_miny": "miny",
                "grid_maxx": "maxx", "grid_maxy": "maxy", "count": "total_count"}, inplace=True)

conn.close()

#save to csv
final_df.to_csv("Counts_output.csv", index=False)

# 轉換成 Polygon（多邊形）
final_df["geometry"] = final_df.apply(
    lambda row: Polygon(
        [
            (row["minx"], row["miny"]),
            (row["maxx"], row["miny"]),
            (row["maxx"], row["maxy"]),
            (row["minx"], row["maxy"]),
            (row["minx"], row["miny"]),  # 關閉多邊形
        ]
    ),
    axis=1,
)

# 轉換成 GeoDataFrame
gdf = gpd.GeoDataFrame(final_df, geometry="geometry", crs="EPSG:4326")

# Ensure total_count is float
gdf["total_count"] = gdf["total_count"].astype(float)


########

# 繪製地圖 (與之前相同)
taiwan_geojson = "/Users/jue-ying/Desktop/Data-Science-Class/GIS/Layers/Geojson_WGS84/Taiwan-County_WGS84.geojson"
taiwan_gdf = gpd.read_file(taiwan_geojson)

fig, ax = plt.subplots(figsize=(10, 8))
taiwan_gdf.plot(ax=ax, color="lightgreen", edgecolor="black", alpha=0.3)

# 繪製熱點圖，並設定圖例位置和尺寸

# Plot the GeoDataFrame with the colorbar
gdf.plot(
    column="total_count", cmap="plasma", linewidth=0.01, edgecolor="black", legend=True, ax=ax,
)

ax.set_title("Spatial-Analysis", fontsize=14)
ax.set_xlim(119, 122.4)
ax.set_ylim(21.5, 25.5)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
plt.show()
