

import os
import pandas as pd


'''
功能介绍：做特征归一化的代码

参数介绍：
fcm_path 流式数据的路径，请勿写绝对路径，写到目录为止即可。示例 fcm_path ='D:/Flow_cytometry_data/fcs_py_and_r/quanx/CSV_2019_2020/'
out_path 输出路径
'''
def fcm_normalize(fcm_path,out_path):
    # 获取目录下所有CSV文件
    files = [f for f in os.listdir(fcm_path) if f.endswith('.csv')]
    for file in files:
        # 读取CSV文件
        df = pd.read_csv(os.path.join(fcm_path, file))

        # 对每一列进行异常值处理和归一化
        for column in df.columns:
            # 计算异常值的范围
            min_value = df[column].quantile(0.025)  # quantile函数是求百分位数的函数
            max_value = df[column].quantile(0.975)

            # 将异常值设为0或1，其余值进行归一化，lambda是创建匿名函数的语法，参数为x
            df[column] = df[column].apply(
                lambda x: 0 if x < min_value else (1 if x > max_value else (x - min_value) / (max_value - min_value)))

        # 将修改后的文件保存到指定目录
        df.to_csv(os.path.join(out_path, file), index=False)