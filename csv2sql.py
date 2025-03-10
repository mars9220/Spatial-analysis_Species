import geopandas as gpd
import sqlite3
import pandas as pd

# 1. 讀取 CSV 檔案 & table名稱
table_name = '哺乳類物種網格'
csv_file = f'/Users/jue-ying/Desktop/Data-Science-Class/GIS/物種多樣性/{table_name}/gridtaxon-1km-raw.csv' # 替換成你的 CSV 檔案
df = pd.read_csv(csv_file)

# 2. 連接 SQLite 資料庫（若無則自動建立）
db_file = "/Users/jue-ying/Desktop/Data-Science-Class/GIS/物種多樣性/biology.sqlite" 
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# 3. 建立 SQL 資料表（假設 CSV 欄位為 id, name, age）
cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        grid_id,grid_minx,grid_miny,grid_maxx,grid_maxy,
        taxon_uuid,taxon_name_scientific_simple,taxon_name_tw
    )
""")

# 4. 將 CSV 數據存入 SQL
df.to_sql(table_name, conn, if_exists="append", index=False)

# 5. 確認資料
print(pd.read_sql(f"SELECT * FROM {table_name}", conn))

# 6. 關閉游標和連線
cursor.close()
conn.close()

print("CSV 已轉換為 SQLite 資料庫")
