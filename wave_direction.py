import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

# 入力ファイルパスと出力ファイルパス
input_path = "/Users/yamaguchitaisei/20241020wave.xlsx"
output_path = "/Users/yamaguchitaisei/20241020wave_direction.png"

# データ読み込み
df = pd.read_excel(input_path)
df.columns = df.columns.str.strip()

# 時刻列作成
df["Time"] = pd.to_datetime(df[["Year", "Month", "Day", "Hour", "Minute", "Second"]])

# Mean Direction をラジアンに変換してベクトル成分を計算
angles_rad = np.deg2rad(df["Mean Direction"])
u = np.sin(angles_rad)  # x方向（東）
v = np.cos(angles_rad)  # y方向（北）

# Y位置を固定（すべて同じ高さに配置）
y = np.ones(len(df))

# プロット
fig, ax = plt.subplots(figsize=(16, 3))
ax.quiver(df["Time"], y, u, v, angles='uv', scale=20, width=0.008, color='red')

# 横軸フォーマットを "MM/DD HH:MM" に設定
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
plt.xticks(rotation=45)

# 左右に時間の余白を追加して矢印の切れを防止
start_time = df["Time"].min() - pd.Timedelta(minutes=20)
end_time = df["Time"].max() + pd.Timedelta(minutes=20)
ax.set_xlim(start_time, end_time)

# グラフ装飾
ax.set_yticks([])
ax.set_title("Mean Wave Direction(2024-10-20)", fontsize=14)
ax.set_xlabel("Time", fontsize=12)
ax.grid(True, axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()

# 保存
plt.savefig(output_path, dpi=300)
print(f"グラフを保存しました: {output_path}")
