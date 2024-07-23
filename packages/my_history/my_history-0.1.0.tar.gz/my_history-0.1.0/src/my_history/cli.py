import pandas as pd

def cnt():
    df = pd.read_parquet("~/tmp/history.parquet")
    fdf = df[df['cmd'].str.contains('aws')]
    cnt = fdf['cnt'].sum()
    print(cnt)
