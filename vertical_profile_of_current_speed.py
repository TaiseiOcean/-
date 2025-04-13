# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 入力ファイルパス
input_path = "/Users/yamaguchitaisei/20241017current.xlsx"

# データの読み込み
df = pd.read_excel(input_path, sheet_name="Sheet1")
df["Time"] = pd.to_datetime(df["DateTime"])

# 流速カラムと水深の抽出
speed_cols = [col for col in df.columns if col.startswith("Speed#")]
depths = np.array([float(col.split("(")[-1].replace("m)", "")) for col in speed_cols])
speed_data = df[speed_cols].to_numpy().T

# 水深を深い順に並べ替え
sort_idx = np.argsort(-depths)
sorted_depths = depths[sort_idx]
sorted_speeds = speed_data[sort_idx, :]
time_data = df["Time"]

# プロット作成
plt.figure(figsize=(14, 6))
plt.pcolormesh(time_data, sorted_depths, sorted_speeds, shading='auto',
               cmap='coolwarm', vmin=0, vmax=1)
plt.colorbar(label='Current Speed (m/s)')
plt.xlabel('Time')
plt.ylabel('Depth (m)')
plt.title('Vertical Profile of Current Speed (2024-10-17)')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
plt.xticks(rotation=45)
plt.tight_layout()

# 出力ファイルパス
output_path = "/Users/yamaguchitaisei/20241017current.png"
plt.savefig(output_path, dpi=300)
plt.close()

print(f"Vertical profile image saved to: {output_path}")
