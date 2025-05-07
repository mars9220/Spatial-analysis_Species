import geopandas as gpd
import sqlite3
import pandas as pd
import json


# 建立資料庫連線
db_file = "/GIS/物種多樣性/biology-all.sqlite"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# 從 JSON 檔案讀取表格名稱
with open("tables.json", "r") as file:
    data = json.load(file)
    file_name = data["table_names"]

# 讀取每個 CSV 檔案並匯入到資料庫
for table_name in file_name:
    print(table_name)
    # 替換成你的 CSV 檔案
    file = f"/GIS/物種多樣性/{table_name}/gridtaxon-1km-raw.csv"
    df = pd.read_csv(file)
    df.to_sql(table_name, conn, if_exists="append", index=False)

    # 5. 確認資料
    print(pd.read_sql(f"SELECT * FROM {table_name}", conn))

# 6. 關閉游標和連線
cursor.close()
conn.close()

print("CSV 已轉換為 SQLite 資料庫")
