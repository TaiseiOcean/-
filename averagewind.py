import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Excelファイルの読み込み
file_path = '/Users/yamaguchitaisei/20241017wind.xlsx'
df = pd.read_excel(file_path)

# 列名のクリーンアップ
df.columns = df.columns.str.replace('"', '').str.strip()

# 日時をdatetime型に変換
df['日時'] = pd.to_datetime(df['日時'])

# グラフの作成
plt.figure(figsize=(12, 6))
plt.plot(df['日時'], df['平均風速 [m/s]'], marker='o', color='gold')
plt.xlabel('DateTime')
plt.ylabel('Wind Speed (m/s)')
plt.title('Average Wind Speed (m/s)')
plt.grid(True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
plt.xticks(rotation=45)
plt.tight_layout()

# 画像ファイルとして保存
output_path = '/Users/yamaguchitaisei/20241017wind.png'
plt.savefig(output_path, dpi=300)

# プロットを表示（任意）
# plt.show()
