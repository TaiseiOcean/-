import pandas as pd

# 入力ファイルのパス
wind_path = "/Users/yamaguchitaisei/20240827wind.xlsx"
current_path = "/Users/yamaguchitaisei/20240827current.xlsx"
output_path = "/Users/yamaguchitaisei/20240827Blowcurrent.xlsx"

# データの読み込み
wind_df = pd.read_excel(wind_path, sheet_name="Sheet1")
current_df = pd.read_excel(current_path, sheet_name="Sheet1")

# 日時をdatetime型に変換
wind_df["Time"] = pd.to_datetime(wind_df.iloc[:, 0])
current_df["Time"] = pd.to_datetime(current_df["DateTime"])

# 列名整備と風速名リネーム
wind_df.columns = [col.strip().replace('"', '') for col in wind_df.columns]
wind_df = wind_df.rename(columns={wind_df.columns[1]: "AvgWind"})

# 流速データ（19.95m）と時間を CurrentTime として保存
speed_df_19m = current_df[["Time", "Speed#19(19.95m)"]].rename(columns={
    "Time": "CurrentTime",
    "Speed#19(19.95m)": "Speed_19m"
})

# 時間でマージ（±5分以内）
merged_df = pd.merge_asof(
    wind_df.sort_values("Time"),
    speed_df_19m.sort_values("CurrentTime"),
    left_on="Time",
    right_on="CurrentTime",
    direction="nearest",
    tolerance=pd.Timedelta("5min")
)

# 条件抽出：潮止まりかつ強風
condition_df = merged_df[
    (merged_df["Speed_19m"] < 0.15) &
    (merged_df["AvgWind"] >= 6.0)
].copy()

# Time を current の元時間に置き換え
condition_df["Time"] = condition_df["CurrentTime"]

# wind_df の 3〜5列目と CurrentTime を削除
columns_to_drop = [wind_df.columns[2], wind_df.columns[3], wind_df.columns[4], "CurrentTime"]
condition_df = condition_df.drop(columns=columns_to_drop, errors="ignore")

# 出力
condition_df.to_excel(output_path, index=False)

print(f"潮止まりかつ強風のデータを以下に保存しました：\n{output_path}")
