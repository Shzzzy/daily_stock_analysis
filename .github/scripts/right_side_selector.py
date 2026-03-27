import akshare as ak
import pandas as pd

def select_right_side():

    df = ak.stock_zh_a_spot_em()

    # 去ST
    df = df[~df['名称'].str.contains('ST')]

    # 成交额过滤（活跃度）
    df = df[df['成交额'] > 5e8]

    # 涨幅过滤（右侧启动）
    df = df[(df['涨跌幅'] > 2) & (df['涨跌幅'] < 8)]

    # 换手率
    df = df[df['换手率'] > 3]

    # 排序
    df = df.sort_values('涨跌幅', ascending=False)

    top50 = df.head(50)['代码'].tolist()

    return ",".join(top50)


if __name__ == "__main__":
    print(select_right_side())
