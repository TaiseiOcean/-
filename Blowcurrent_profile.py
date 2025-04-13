import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# ファイルパスの指定
current_path = "/Users/yamaguchitaisei/20241017current.xlsx"
blow_path = "/Users/yamaguchitaisei/20241017Blowcurrent.xlsx"
output_path = "/Users/yamaguchitaisei/20241017Blowcurrent_profile.png"

# データの読み込み
current_df = pd.read_excel(current_path, sheet_name="Sheet1")
blow_df = pd.read_excel(blow_path)

# 時刻の整形
current_df["Time"] = pd.to_datetime(current_df["DateTime"])
target_times = pd.to_datetime(blow_df.iloc[2:9, 2])  # 3列目の1〜5行目（0-indexed）

# 指定時刻に最も近い current データを抽出
matched_profiles = []
matched_times = []

for t in target_times:
    idx = (current_df["Time"] - t).abs().idxmin()
    matched_profiles.append(current_df.loc[idx])
    matched_times.append(current_df.loc[idx, "Time"])

matched_df = pd.DataFrame(matched_profiles)

# 流速カラムと水深の抽出
speed_cols = [col for col in matched_df.columns if col.startswith("Speed#")]
depths = np.array([float(col.split("(")[-1].replace("m)", "")) for col in speed_cols])
speed_array = matched_df[speed_cols].to_numpy().T

# 水深を深い順に並べ替え
sort_idx = np.argsort(-depths)
sorted_depths = depths[sort_idx]
sorted_speeds = speed_array[sort_idx, :]

# プロット作成（上下反転しない）
plt.figure(figsize=(12, 6))
colors = cm.coolwarm(np.linspace(0, 1, len(matched_times)))

for i, time in enumerate(matched_times):
    plt.plot(sorted_speeds[:, i], sorted_depths, label=time.strftime("%H:%M"), color=colors[i])

plt.xlabel("Current Speed (m/s)")
plt.ylabel("Depth (m)")
plt.title("Blow Current Vertical Profiles (2024-10-20)")
plt.legend(title="Time", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()

# 画像として保存（PNG形式）
plt.savefig(output_path, dpi=300)
plt.close()

print(f"Blow Current プロファイル画像を保存しました：{output_path}")
