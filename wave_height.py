import pandas as pd
import matplotlib.pyplot as plt

# 入力ファイルパスと出力ファイルパス
input_path = "/Users/yamaguchitaisei/20240828wave.xlsx"
output_path = "/Users/yamaguchitaisei/202408280wave.png"

# Excelファイル読み込み
df = pd.read_excel(input_path)

# 列名の前後の空白を削除（必要に応じて）
df.columns = df.columns.str.strip()

# 日時データを結合して Time 列を作成
df["Time"] = pd.to_datetime(df[["Year", "Month", "Day", "Hour", "Minute", "Second"]])
df["TimeLabel"] = df["Time"].dt.strftime("%m-%d %H:%M:%S")

# グラフ描画
plt.figure(figsize=(12, 6))
plt.plot(df["TimeLabel"], df["Significant Height(Hm0)"], marker="o", color="red")
plt.title("Significant Wave Height (Hm0)", fontsize=14, fontweight='bold')
plt.xlabel("Time", fontsize=12, fontweight='bold')
plt.ylabel("Significant Height (Hm0) [m]", fontsize=12, fontweight='bold')
plt.grid(True)
plt.xticks(rotation=60, fontsize=10, fontweight='bold')
plt.yticks(fontsize=10, fontweight='bold')
plt.tight_layout()

# グラフをファイルに保存
plt.savefig(output_path)
print(f"保存完了: {output_path}")
