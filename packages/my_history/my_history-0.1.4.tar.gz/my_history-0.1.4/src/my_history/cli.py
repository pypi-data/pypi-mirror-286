import pandas as pd
import sys

def cnt():
    df = pd.read_parquet("~/tmp/history.parquet")
    fdf = df[df['cmd'].str.contains(sys.argv[1])]
    cnt = fdf['cnt'].astype(int).sum()
    print(cnt)
