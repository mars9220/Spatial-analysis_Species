import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# 讀取數據
df = pd.read_csv("Counts_output.csv", encoding="big5")

# 計算統計數據
mean_val = np.mean(df["total_count"])
std_val = np.std(df["total_count"])
min_val = np.min(df["total_count"])
max_val = np.max(df["total_count"])
len_val = len(df["total_count"])

# 繪製直方圖
plt.figure(figsize=(10, 6))
ax = sns.histplot(df["total_count"], bins=59, kde=True, color="skyblue")
ax.lines[0].set_color('crimson')

# 加入統計數據到圖表
stats_text = f"Mean: {mean_val:.2f}\nStd: {std_val:.2f}\nMin: {min_val}\nMax: {max_val}\nCount: {len_val}"
ax.text(0.95, 0.95, stats_text, transform=ax.transAxes, fontsize=12,
        verticalalignment='top', horizontalalignment='right', 
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))

# 標題與軸標籤
ax.set_title("Distribution of Total Count")
ax.set_xlabel("Total Count")
ax.set_ylabel("Frequency")

plt.show()
