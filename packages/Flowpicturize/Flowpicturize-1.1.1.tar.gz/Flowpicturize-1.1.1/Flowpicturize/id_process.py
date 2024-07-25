
import pandas as pd
'''
在需要过采样的时候，由于细胞数量巨大，可通过切片操作把患者id切割成多部分，然后在多个进程上运行，以提高运行效率
'''
'''
使用该工具前请先保证pandas库的安装与兼容
参数介绍： 
data_list 为你的患者id的集合，希望是list格式
cut_num 是你需要切割的次数 譬如你将来希望工作在3个进程上运行 就把cut_num设置为3
'''
def id_cut(data_list, cut_num):
    total_length = len(data_list)
    part_length = total_length // cut_num

    # 切片成多个部分
    parts = [data_list[i * part_length:(i + 1) * part_length] for i in range(cut_num)]

    return parts


'''
功能介绍：这是提取csv文件中id的函数，并按升序排列，以方便在训练模型等操作时按一定顺序索引患者

csv_file 为你的元文件
ID 为你的id列或索引列的列名
'''
def extract_and_sort_ids(csv_file,ID:str):
    try:
        # 读取 CSV 文件
        data = pd.read_csv(csv_file)

        # 提取 'id' 列并转换成列表，并按升序排列
        sorted_ids = sorted(data[f'{ID}'].tolist())

        return sorted_ids
    except Exception as e:
        print("Error:", e)
        return []


'''
# 示例用法
# 假设 who_2020_train 是你的数据列表
list_train = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 切片成四部分
cut_num = 4
sliced_parts = id_cut(list_train, cut_num)
print(sliced_parts)
'''