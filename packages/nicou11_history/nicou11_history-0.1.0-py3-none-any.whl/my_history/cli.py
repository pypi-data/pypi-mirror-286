import pandas as pd
import sys

INPUT = sys.argv[1]

def cnt():
    #INPUT = sys.argv[1]
    df = pd.read_parquet("~/tmp/history.parquet")
    fdf = df[df['cmd'].str.contains(INPUT)]
    cnt = fdf['cnt'].sum()
    print(cnt)
