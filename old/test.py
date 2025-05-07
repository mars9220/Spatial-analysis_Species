import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from shapely.geometry import Polygon

# 讀取 CSV 檔案
csv_file = '/GIS/物種多樣性/蝦蟹類/蝦蟹類-data.csv'  # 請替換成你的 CSV 檔案路徑
df = pd.read_csv(csv_file)


# 確保 CSV 包含所需的欄位
required_columns = {'minx', 'miny', 'maxx', 'maxy'}
if not required_columns.issubset(df.columns):
    raise ValueError(f"CSV 檔案缺少必要的欄位: {required_columns - set(df.columns)}")

# 建立 GeoDataFrame，將每個範圍轉換為矩形（Polygon）
def create_polygon(row):
    return Polygon([
        (row['minx'], row['miny']),
        (row['maxx'], row['miny']),
        (row['maxx'], row['maxy']),
        (row['minx'], row['maxy']),
        (row['minx'], row['miny'])  # 關閉多邊形
    ])

df["geometry"] = df.apply(create_polygon, axis=1)
gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")

# 設定熱點值（假設 CSV 有 "count" 欄位，否則我們可以用區域密度來計算）
if "count" not in df.columns:
    gdf["count"] = 1  # 如果沒有計數欄位，則假設每個區域計數為 1

# 設定地圖大小
fig, ax = plt.subplots(figsize=(10, 8))

# 繪製熱點圖（以 count 值作為顏色變數）
gdf.plot(column="count", cmap="Reds", linewidth=0.5, edgecolor="black", legend=True, ax=ax)

# 設定標題與座標
ax.set_title("熱點圖（基於最大/最小經緯度範圍）", fontsize=14)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()
