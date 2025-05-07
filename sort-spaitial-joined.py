import geopandas as gpd
import sqlite3
import pandas as pd
import json

# 1. 讀取 GeoJSON 檔案
layer1 = gpd.read_file(
    "/GIS/物種多樣性/Species-Spaitial-total-count.geojson"
)
layer2 = gpd.read_file("/GIS/TSMC/TSMC-loc-3-Buffered.geojson")

# 2. 執行空間相交 (Spatial Join)
joined_data = gpd.sjoin(layer1, layer2, how="inner", predicate="intersects")

# 3. 儲存相交後的 GeoJSON
joined_data.to_file("joined_data-loc3.geojson", driver="GeoJSON")

# 4. 讀取剛剛生成的 GeoJSON
file_path = "joined_data-loc3.geojson"

with open(file_path, "r", encoding="utf-8") as f:
    geojson_data = json.load(f)

# 5. 讀取要查詢的資料表名稱
with open("tables.json", "r") as file:
    data = json.load(file)
    table_names = data["table_names"]

# 6. 連接 SQLite
db_file = "/GIS/物種多樣性/biology-all.sqlite"
conn = sqlite3.connect(db_file)

# 7. 收集所有 `grid_id`，避免重複查詢
unique_grid_ids = {feature["properties"]["grid_id"] for feature in geojson_data["features"]}
grid_id_to_name = {feature["properties"]["grid_id"]: feature["properties"]["name"] for feature in geojson_data["features"]}


# 8. 執行 SQL 查詢
all_results = []  # 用來存儲所有查詢結果

for grid_id in unique_grid_ids:
    for table_name in table_names:
        sql_query = f"""
        SELECT
            grid_id,
            grid_minx,
            grid_miny,
            grid_maxx,
            grid_maxy,
            taxon_uuid,
            '{table_name}' AS 物種名,
            taxon_name_tw,
            國內紅皮書評估類別
        FROM {table_name}
        JOIN 國內紅皮書名錄 on 物種UUID = taxon_uuid
        WHERE grid_id = '{grid_id}'
        AND 國內紅皮書評估類別 IN ('易危（VU, Vulnerable）', '瀕危（EN, Endangered）', '極危（CR, Critically Endangered）')
        """
        df = pd.read_sql(sql_query, conn)
        all_results.append(df)  # 儲存結果

# 9. 合併所有結果
if all_results:
    final_df = pd.concat(all_results, ignore_index=True)

    # 10. 新增 unique_grid_name 欄位
    final_df["unique_grid_name"] = final_df["grid_id"].map(grid_id_to_name)

    # 11. 儲存為 CSV
    final_df.to_csv("joined-company-species-loc3.csv", index=False, encoding="utf-8")
    print(f"結果已儲存至 'joined-company-species-loc3.csv'，共 {len(final_df)} 筆資料。")
else:
    print("沒有符合條件的資料！")

# 12. 關閉資料庫連線
conn.close()
