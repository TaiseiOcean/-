import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ===== ファイルパス =====
wind_file = "/Users/yamaguchitaisei/20240807wind.xlsx"
current_file = "/Users/yamaguchitaisei/20240807current.xlsx"
output_image_path = "/Users/yamaguchitaisei/20240807direction.png"

# ===== 1. データ読み込み =====
df_wind = pd.read_excel(wind_file)
df_current = pd.read_excel(current_file)

# ===== 2. 列の整形と日付変換 =====
df_wind.columns = df_wind.columns.str.replace('"', '').str.strip().str.replace("　", "").str.replace(" ", "")
df_current.columns = df_current.columns.str.strip()

df_wind["日時"] = pd.to_datetime(df_wind["日時"])
df_current["DateTime"] = pd.to_datetime(df_current["DateTime"])

# ===== 3. 平均風向に +180°して風が向かう方向に =====
df_wind["平均風向"] = pd.to_numeric(df_wind["平均風向[°]"], errors='coerce')
df_wind["風向修正"] = (df_wind["平均風向"] + 180) % 360

# ===== 4. 加重平均流向の計算 =====
speed_cols = [col for col in df_current.columns if "Speed#" in col]
dir_cols = [col for col in df_current.columns if "Dir#" in col]

# 数値変換（安全に）
df_current[speed_cols] = df_current[speed_cols].apply(pd.to_numeric, errors='coerce')
df_current[dir_cols] = df_current[dir_cols].apply(pd.to_numeric, errors='coerce')

def compute_weighted_direction(row):
    speeds = row[speed_cols].astype(float).values
    directions_deg = row[dir_cols].astype(float).values
    mask = (~np.isnan(speeds)) & (~np.isnan(directions_deg))
    if not np.any(mask):
        return np.nan
    speeds = speeds[mask]
    directions_rad = np.deg2rad(directions_deg[mask])
    x = np.sum(speeds * np.cos(directions_rad))
    y = np.sum(speeds * np.sin(directions_rad))
    total_speed = np.sum(speeds)
    if total_speed == 0:
        return np.nan
    mean_rad = np.arctan2(y / total_speed, x / total_speed)
    return (np.degrees(mean_rad) + 360) % 360

df_current["Weighted Mean Direction"] = df_current.apply(compute_weighted_direction, axis=1)

# ===== 5. ベクトル成分の計算 =====
u_current = np.cos(np.deg2rad(df_current["Weighted Mean Direction"]))
v_current = np.sin(np.deg2rad(df_current["Weighted Mean Direction"]))
times_current = df_current["DateTime"]

u_wind = np.cos(np.deg2rad(df_wind["風向修正"]))
v_wind = np.sin(np.deg2rad(df_wind["風向修正"]))
times_wind = df_wind["日時"]

# ===== 6. 間引き処理 =====
step_current = max(len(times_current) // 50, 1)
step_wind = max(len(times_wind) // 50, 1)

times_current_sampled = times_current[::step_current]
u_current_sampled = u_current[::step_current]
v_current_sampled = v_current[::step_current]

times_wind_sampled = times_wind[::step_wind]
u_wind_sampled = u_wind[::step_wind]
v_wind_sampled = v_wind[::step_wind]

# ===== 7. グラフ描画と保存 =====
plt.figure(figsize=(15, 4))
plt.quiver(times_current_sampled, np.zeros_like(times_current_sampled),
           u_current_sampled, v_current_sampled, scale=20, width=0.005,
           color='blue', label='Current Direction')

plt.quiver(times_wind_sampled, np.zeros_like(times_wind_sampled),
           u_wind_sampled, v_wind_sampled, scale=20, width=0.005,
           color='gray', label='Average Wind Direction (+180°)')

plt.title("Comparison of Current and Wind Directions (2024/08/07)")
plt.xlabel("Time")
plt.ylabel("Direction Vector")
plt.yticks([])
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
plt.grid(True)
plt.legend()
plt.tight_layout()

# 保存
plt.savefig(output_image_path)
plt.close()
