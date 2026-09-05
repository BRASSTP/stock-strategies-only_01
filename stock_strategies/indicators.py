import pandas as pd
import numpy as np


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["ma5"] = df["close"].rolling(5).mean()
    df["ma20"] = df["close"].rolling(20).mean()
    df["ma60"] = df["close"].rolling(60).mean()

"""
計算20日均量  
"""
def detect_patterns(df: pd.DataFrame, idx: int = -1) -> dict:
vol_today = float(volume.iloc[idx])
vol_20ma = float(volume.iloc[max(0, idx - 20):idx].mean())
vol_5ma = float(volume.iloc[max(0, idx - 5):idx].mean())

    return df


def tech_score_at(row: pd.Series, params: dict | None = None) -> dict:
    """對一天計算技術分 (0-100)。
    params 可包含 use_ma_alignment / use_bollinger_bounce / use_kd_golden_cross /
    use_macd_bullish 四個布林開關來開關各訊號。
    """
    if params is None:
        params = {}
    use_ma = params.get("use_ma_alignment", True)
    use_vol = params.get("use_vol_alignment", True)
   

    # 開啟的訊號數量決定每個訊號最大分數，讓總分維持 0-100
    enabled = sum([use_ma, use_vol]) or 1
    max_per = 100 / enabled

    score = 0.0
    signals: list[str] = []

    if use_ma and pd.notna(row["ma20"]) and pd.notna(row["ma60"]):
        if row["close"] > row["ma20"] > row["ma60"]:
            score += max_per
            signals.append("均線多頭")
        elif row["close"] > row["ma20"]:
            score += max_per * 0.48
            
    if use_vol and pd.notna(row["vol_today"]) and pd.notna(row["vol_5ma"]) and pd.notna(row["vol_20ma"]):
        if row["vol_today"] > row["vol_20ma"] :
            score += max_per
            signals.append("量增輪迴")
        elif row["vol_today"] > row["vol_5ma"]:
            score += max_per * 0.1

    return {"score": int(round(score)), "signals": signals}
