import geopandas as gpd
import sqlite3
import pandas as pd

# 1. 讀取 CSV 檔案 & table名稱
table_name = '國內紅皮書名錄'
csv_file = f'/GIS/物種多樣性/國內紅皮書-名錄/data.csv' 
df = pd.read_csv(csv_file)

# 2. 連接 SQLite 資料庫（若無則自動建立）
db_file = "/GIS/物種多樣性/biology-all.sqlite" 
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# 3. 建立 SQL 資料表
cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        物種UUID, 分類階層, 類群, 科, 科中文名,
        分類群學名, 分類群俗名, 簡學名, 特有性, 原生性, 保育類等級, 國內紅皮書評估類別
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
