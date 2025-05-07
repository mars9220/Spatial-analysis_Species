# Biodiversity Sensitivity Analysis in Taiwan

This project leverages the data from the **Taiwan Biodiversity Network Database** provided by the Agricultural Research Institute to analyze the presence of threatened species (CR, EN, VU) as listed in the Domestic Red List. The objective is to assess species sensitivity in specific target areas by classifying species into four quartiles: VH (Very High), H (High), M (Medium), and L (Low). This approach aims to support spatial analysis for conservation and land management purposes.

## Workflow

### 1. Data Collection and Database Creation

* Extract data from the Taiwan Biodiversity Network Database for the period **March 2015 - March 2025**, focusing on 1km grid species data.
* Adjust the folder names for data consistency.
* Create a SQLite database `biology-all.sqlite` to store species data and Red List information.

**Data Processing Steps:**

* Run [csv2sql-name.py](/csv2sql-name.py) to convert `國內紅皮書-名錄/data.csv` into a SQL table named `國內紅皮書名錄`.

  * Columns include:

    * `UUID`, `Classification Level`, `Taxon`, `Family`, `Family (Chinese)`, `Scientific Name`, `Common Name (Chinese)`, `Simple Scientific Name`, `Endemic Status`, `Native Status`, `Conservation Level`, `Red List Category`

* Execute [csv2sql-Batchfile.py](/csv2sql-Batchfile.py) to create tables for each species based on the grid data found in `gridtaxon-1km-raw.csv`.

  * Columns include:

    * `grid_id`: Grid identifier
    * `grid_minx`, `grid_miny`, `grid_maxx`, `grid_maxy`: Bounding box coordinates
    * `taxon_uuid`: Species UUID
    * `taxon_name_scientific_simple`: Simple scientific name
    * `taxon_name_tw`: Common name in Chinese

### 2. Data Filtering and Spatial Analysis

* Identify threatened species by querying the Red List data.
* Filter species with CR, EN, or VU status using `plot-count-sql-Batchfile.py`.
* Aggregate species data by grid and calculate occurrence counts.
* Convert grid data to polygon shapes for spatial visualization.
* Visualize the spatial distribution of threatened species using the base map of Taiwan. **Output: `/Figure_1`**

### 3. Histogram Analysis

* Execute `read-plot-histogram.py` to generate histograms of species occurrence across grids.
* Analyze distribution patterns to optimize spatial representation. **Output: `/Figure_2.png`**

### 4. Target Area Analysis

* Overlay the target area with grid data to assess potentially impacted species.
* Run `sort-spatial-joined.py` to extract affected grids and output the data as a CSV file for further spatial analysis in QGIS.


# Spatial-analysis_species

使用農業部生物多樣性研究所「台灣生物多樣性網絡資料」分析區域是否存在國內紅皮書受脅評估為瀕危(CR)、極危(EN) 或易危(VU) 等級的動植物。將物種劃分四分位數,並分別訂為物種敏感度VH、H、M、L。希望藉此來分析目標場域內的物種敏感度，
操作步驟為抓取近10年內的1km網格資料，透過國內紅皮書篩選出受威脅的物種，建立對應資料庫，以利後續的場域資料分析。

1. 資料清洗 ＆ 建立資料庫：
- 從「台灣生物多樣性網絡資料」篩選 2015/03 - 2025/03 的 1km 網格物種資料，校正資料夾名稱。
- 製作資料庫"biology-all.sqlite"，並建立對應的 紅皮書物種名稱table 與 各物種資料庫。
- 跑 "csv2sql-name.py"(#csv2sql-name.py)可以將 '國內紅皮書-名錄/data.csv' 轉至SQL。
  table_name = '國內紅皮書名錄'，欄位依序為 「物種UUID,分類階層,類群,科,科中文名,分類群學名,分類群俗名,簡學名,特有性,原生性,保育類等級,國內紅皮書評估類別」
- 跑 “csv2sql-Batchfile.py”將各物種資料夾中'gridtaxon-1km-raw.csv'，依照物種名稱命名table。
  內有物種資訊與格點資訊：
            "grid_id": 網格編號, "grid_minx": 最小經度, "grid_miny": 最小緯度, "grid_maxx": 最大經度, "grid_maxy": 最大緯度,...
            "taxon_uuid": 物種TBN UUID,"taxon_name_scientific_simple": 簡學名, "taxon_name_tw": 中文俗名
  
2. 透過資料庫篩選資料，繪製出空間資料情形：
- 跑 "plot-count-sql-Batchfile.py": 透過 table_name=國內紅皮書名錄 篩選受脅評估為瀕危(CR)、極危(EN) 或易危(VU) 等級的「物種UUID」，並利用計算同網格的數量。透過在將同網格的透過位置資訊轉換成多邊形網格，繪製出對應的空間資料結果。最後以台灣為底圖，繪製出對應的空間資訊。
/Figure_1

- 跑 “read-plot-histogram.py": 繪製格點分佈的直方圖，分析適合的統計分析，用於空間呈現上的優化。
  ![/figure2]/Figure_2.png

3. 目標場域的周遭情況分析，透過目標場域的位置，跟網格做疊加分析，篩選出可能受影響的物種所在網格。
   - 跑“sort-spaitial-joined.py"篩選出受影響的網格資料，並輸出成 CSV 以利於用 QGIS 做空間分析。


