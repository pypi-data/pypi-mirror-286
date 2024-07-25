import os
import pandas as pd
import random
import jieba
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from typing import List, Callable
# 在R中使用Flowcore包把fcm文件以csv格式写入一个目录后，可使用该模块的功能，把流式数据的讯息按自拟定的分辨率映射在图片数据结构的四维张量中
random.seed(42)
'''
make_grid函数功能解释：
将流式细胞数据中各个抗原参数视为红、绿、蓝这样的颜色通道，并把兼顾细胞粒度与免疫类型的SSC-A参数和CD45抗原按从小到大的顺序分为若干个组段，以形成一个自拟定分辨率的像素矩阵平面。在像素矩阵平面上，逐一扫描每个SSC-A/CD45位点，从每个位点对应的范围内随机选取患者的细胞，并将其抗原表达量填入该位点，各抗原通道重叠后的这个像素点就是患者的综合免疫特征。如果位点没有细胞，则将抗原表达量设为0。
使用此工具前，请先保证os、pandas、random、jieba、keras、typing等库的安装和兼容

各参数解释：
data_path 是你的csv文件的路径
axial_variable 是你用作坐标轴的变量，必须是两个字符串的元组，请填写两个字符串。示例：axial_variable = 'SSC-A','CD45'
tube_variable 是你需要提取特征的抗原或者参数
Resolution 是你想要拟定图片的分辨率
over_sampling 是选择是否过采样，如果过采样填Ture，将取抽样细胞群的随机值，否则False，将取抽样细胞群的中位数。
sampling_num 是输出文件过采样后的id
id 是患者编号，如不填默认为‘id’
year 是数据的年份，如不填默认为‘year’
'''
def mkgrid(data_path,axial_variable: tuple[str, str],tube_variable:str,Resolution,over_sampling: bool,sampling_num='num',Id='id',year='year'):
    # 如果不执行过采样，执行以下代码。通常对测试集这么做。
    if over_sampling == False:
        # 创建输出目录
        out_path = f"no_oversampling_path/{int(Resolution)}*{int(Resolution)}"
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        # 检查文件路径
        if not os.path.exists(data_path):
            print(f"File {data_path} does not exist.")
            return
        data_path = data_path
        data = pd.read_csv(data_path)
        Resolution_reciprocal = 1 / Resolution
        # 定义条件
        conditions = [
            (f'{i}/{Resolution}, {i + 1}/{Resolution}', Resolution_reciprocal * i, Resolution_reciprocal * (i + 1)) for
            i in range(0, Resolution)]

        # 将两个元组中的元素合并成一个列表
        combined_columns = list(axial_variable) + list(tube_variable)
        # 创建 DataFrame，并指定列名为合并后的列表
        result = pd.DataFrame(columns=combined_columns)

        # 对每个条件一和条件二的组合进行遍历
        for condition_1 in conditions:
            for condition_2 in conditions:
                # 提取满足条件一和条件二的行
                filtered_data = data[(data[f'{axial_variable[0]}'] > condition_1[1]) & (data[f'{axial_variable[0]}'] <= condition_1[2]) &
                                     (data[f'{axial_variable[1]}'] > condition_2[1]) & (data[f'{axial_variable[1]}'] <= condition_2[2])]

                # 计算筛选行的数据的中位数
                medians = filtered_data[list(tube_variable)].median()
                # 创建一个字典，将 'SSC-A' 和 'CD45' 与 'tube_variable' 对应的中位数组合起来
                new_row = {
                    'SSC-A': condition_1[0],  #
                    'CD45': condition_2[0]  #
                }
                # 使用循环将 tube_variable 中的每个变量及其对应的中位数添加到 new_row 中
                for idx, var in enumerate(tube_variable):
                    new_row[var] = medians[idx]
                # 将新的一行数据追加到 result DataFrame 中
                result = result.append(new_row, ignore_index=True)
        # 将结果保存到新的CSV文件中
        result.to_csv(
            f"{out_path}/grid-{year}-sample-{Id}-{tube_variable}.csv",
            index=False)

    # 如果过采样执行以下代码，通常对训练集这么做
    if over_sampling == True:
        # 创建输出目录
        out_path_2 = f"oversampling_path/{int(Resolution)}*{int(Resolution)}"
        if not os.path.exists(out_path_2):
            os.makedirs(out_path_2)
        # 检查文件路径
        if not os.path.exists(data_path):
            print(f"File {data_path} does not exist.")
            return
        data_path = data_path
        data = pd.read_csv(data_path)
        Resolution_reciprocal = 1 / Resolution
        # 定义条件
        conditions = [
            (f'{i}/{Resolution}, {i + 1}/{Resolution}', Resolution_reciprocal * i, Resolution_reciprocal * (i + 1)) for
            i in range(0, Resolution)]

        # 将两个元组中的元素合并成一个列表
        combined_columns = list(axial_variable) + list(tube_variable)
        # 创建 DataFrame，并指定列名为合并后的列表
        result = pd.DataFrame(columns=combined_columns)

        # 对每个条件一和条件二的组合进行遍历
        for condition_1 in conditions:
            for condition_2 in conditions:
                # 提取满足条件一和条件二的行
                filtered_data = data[
                    (data[f'{axial_variable[0]}'] > condition_1[1]) & (data[f'{axial_variable[0]}'] <= condition_1[2]) &
                    (data[f'{axial_variable[1]}'] > condition_2[1]) & (data[f'{axial_variable[1]}'] <= condition_2[2])]
                # 随机抽取一个数
                if filtered_data.empty:
                    random_values = [0] * 6  # 全部为0的列表
                else:
                    random_values = [random.choice(filtered_data[col].values) for col in list(tube_variable)]
                # 创建一个字典
                new_row = {'SSC-A': condition_1[0],  'CD45': condition_2[0] }
                # 使用循环将 tube_variable 中的每个变量及其对应的抽样值添加到 new_row 中
                for idx, var in enumerate(tube_variable):
                    new_row[var] = random_values[idx]
                # 将新的一行数据追加到 result DataFrame 中
                result = result.append(new_row, ignore_index=True)
                # 将结果保存到新的CSV文件中
                result.to_csv(
                    f"{out_path_2}/grid-{year}-sample-{id}-{tube_variable}.csv",
                    index=False)

    print(f'have finished a {int(Resolution)}*{int(Resolution)} grid ')



'''以下函数为文字数据的重构，使用Jieba分词函数将其分割成若干词段，并用Tokenizer工具编码，保留频率排名前6000的词。'''

# 使用Jieba分词函数分词,并剔除停用词
def txt_cut(juzi,juzi_path):
    stop_list = pd.read_csv(juzi_path, index_col=False,
                            quoting=3,
                            sep="\t", names=['stopword'], encoding='utf-8')  # names参数是指定一个列名，将内容保存到此，quoting是引用字 \n
    lis =[w for w in jieba.lcut(juzi) if w not in stop_list.values]#使用列表推导式,剔除停用词
    return " ".join(lis)

'''
使用以下工具前先创建一个空数据框，示例：my_df_train = pd.DataFrame(columns=['ID', '结果'])
各参数解释：
file_path 你的文件路径
ID 患者索引
ID_column 患者ID那列的列名
outcome_colum 需要输出列的列名
my_df 你的空数据框，列名自拟定，示例 my_df = pd.DataFrame(columns=['ID', '结果']
'''
# 文字读取装进数据框
def NL_to_df(file_path, ID, ID_column, outcome_column, my_df):
    # 读取 CSV 或 Excel 文件
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")

    # 根据 ID_column 列筛选出对应 ID 的行
    filtered_row = df[df[ID_column] == ID]

    if not filtered_row.empty:
        # 获取筛选行中 outcome_column 列的内容作为字符串
        outcome_text = filtered_row[outcome_column].values[0] # 这里对筛选行进行索引，由于系统认为该行可能是二维张量，所以需要指定取值第一行

        # 使用 txt_cut 函数处理文本,并创建一个dict，方便后续append填充
        processed_text = {'ID': ID, '结果': txt_cut(outcome_text)}

        # 将处理后的文本填充到 my_df 数据框的“结果”列下
        my_df = my_df.append(processed_text, ignore_index=True)

        return my_df
    else:
        print(f"No rows found with ID: {ID}")
        return None

'''
my_df 是含文字的数据框
outcome 是你数据框输出列的列名
pad_num 是你的填充长度，使数据更整齐。如100
'''
def token_NL(my_df,outcome:str,pad_num:int):
    my_df_outcome = my_df[f'{outcome}']
    # 初始化 Tokenizer
    tok = Tokenizer(num_words=6000)
    # 对所有数据进行编码
    tok.fit_on_texts(my_df_outcome.values)
    # 文本序列转换为数字序列
    num_train_outcome = tok.texts_to_sequences(my_df_outcome.values)
    # 将序列数据填充成相同长度
    num_train_outcome = pad_sequences(num_train_outcome, maxlen=pad_num)

'''
功能介绍：实现过采样的函数
id_list 你的患者索引列表
meta_file 是你的元文件 应该包括患者索引和诊断结果
id 是患者索引
label 是患者类型
my_df 是你期望的输出位置，请用数据框格式
type 是过采样所对应的类型，如[1,2]，表示患者标签为1或者2，就执行该步骤
freq 是有放回的重复采样次数
function 是你想实现的功能函数,请先将函数实例化。示例：function = token_NL(file_path, who, ID_column, outcome_column, my_df_train)
'''
def id_over_sampling(id_list,meta_file,id,label,my_df,type:list[int],freq,function: Callable):
    # 检查 function 是否是可调用对象
    if not callable(function):
        raise TypeError("function must be a callable object")

    for who in id_list:
        # 如果是type类型，就抽取freq次
        if not meta_file.loc[(meta_file[f'{id}'] == who) & (meta_file[f'{label}'].isin(type))].empty:
            for i in range(freq):
                my_df = function()


'''
功能介绍：
该工具只用于使用mkgrid函数后，对各管型的数据合并。所以使用之前，请务必确保已使用mkgrid函数创建了初始文件。

参数解释：
id_list 包含患者id的列表，请确保已经按照升序或降序等你有把握的顺序排列好
tubes_list 包含各管型变量的列表，示例tubes_list = [[CD38,CD3,CD7],['CD33', 'HLA-DR', 'CD11b']]
其余参数同mkgrid函数
'''
def tube_merged(id_list,tubes_list,Resolution,over_sampling:bool,year='year') :
    if over_sampling == False:
        # 创建输出目录
        out_path = f'merged/no_oversampling_path/{int(Resolution)}*{int(Resolution)}'
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        for who in id_list:

            final_df = pd.DataFrame()
            for tube in tubes_list:
                file_path = f"no_oversampling_path/{int(Resolution)}*{int(Resolution)}/grid-{year}-sample-{who}-{tube}.csv"

                # 设置要读取的文件路径
                if os.path.exists(file_path):

                    # 使用Pandas读取CSV文件
                    df_1 = pd.read_csv(file_path)
                    # 根据需要提取的列进行拼接
                    df_concat = df_1[tube]

                    # 将该文件拼接到最终结果中
                    final_df = pd.concat([final_df, df_concat], axis=1)
                    # 将结果保存为CSV文件
                    output_file = f"{out_path}/grid-{year}-sample-{who}.csv"
                    final_df.to_csv(output_file, index=False)
                else:
                    print('without this num or who')

    if over_sampling == True:
        # 创建输出目录
        out_path_2 = f'merged/oversampling_path/{int(Resolution)}*{int(Resolution)}'
        if not os.path.exists(out_path_2):
            os.makedirs(out_path_2)
        for who in id_list:

            final_df = pd.DataFrame()
            for tube in tubes_list:
                file_path = f"oversampling_path/{int(Resolution)}*{int(Resolution)}/grid-{year}-sample-{who}-{tube}.csv"

                # 设置要读取的文件路径
                if os.path.exists(file_path):

                    # 使用Pandas读取CSV文件
                    df_1 = pd.read_csv(file_path)
                    # 根据需要提取的列进行拼接
                    df_concat = df_1[tube]

                    # 将该文件拼接到最终结果中
                    final_df = pd.concat([final_df, df_concat], axis=1)
                    # 将结果保存为CSV文件
                    output_file = f"{out_path_2}/grid-{year}-sample-{who}.csv"
                    final_df.to_csv(output_file, index=False)
                else:
                    print('without this num or who')


'''
功能介绍：
获取 列标签 的数据，并转换为 numpy数组的函数
参数解释：
file_path 为文件路径
unique_variable 为需要处理的变量，示例：unique_variable = ['CD38', 'CD10', 'CD34', 'CD19', 'CD138', 'CD20']
'''
# 做压缩数组的函数
def my_numpy(file_path,unique_variable):

    #读取csv文件
    data = pd.read_csv(file_path)

    #填充缺失值
    data.fillna(0, inplace=True)

    # 获取 列标签 的数据，并转换为 numpy数组
    unique_variable_data = data[unique_variable].to_numpy()

    # 根据需要调整数组形状
    array = unique_variable_data.reshape((32, 32, len(unique_variable)))

    return array
