import numpy as np
import json
import itertools
import random
from scipy import stats
#
# sentences = []
# # 创建随机数
# for i in range(1,50):
#     sentences.append(f"S{i}")
#
# conbinations = list(itertools.combinations(sentences,2))
#
# data = {}
# for i in conbinations:
#     data[f"{i[0]},{i[1]}"] = random.uniform(0.6,1)
#
# data = json.dumps(data)
#
# with open("data_.json","w",encoding="utf-8") as f:
#     f.write(data)
# f.close()



sentences = []
# 创建随机数
for i in range(1,50):
    sentences.append(f"S{i}")

ret = {}

with open("data_.json","r",encoding="utf-8") as f:
    data = json.load(f)

# data = dict(data[0])
data_ = sorted(data.items(),key= lambda x:x[1],reverse=True)

# 取众数
def get_mode(data_):
    keys_id = []
    for i in data_:
        if i[1] < 0.8:
            break
        Sx, Sy = i[0].split(",")[0],i[0].split(",")[1]
        keys_id.append(Sx)
        keys_id.append(Sy)

    def top1(lst):
        return stats.mode(lst)[0][0]
    return top1(keys_id)

# 聚类
def rest(n=-1):
    n_ = 0
    while 1:
        if n_ == n:
            break
        if len(data_) == 0:
            break
        if data_[0][1] < 0.8:
            break
        mode = get_mode(data_)
        remove_data = []
        remove = []
        clustering = []
        for i in data_:
            if i[1] < 0.8:
                break
            if mode in i[0]:
                Sx, Sy = i[0].split(",")[0], i[0].split(",")[1]
                if Sx != mode and Sx not in remove_data:
                    remove_data.append(Sx)
                if Sy != mode and Sy not in remove_data:
                    remove_data.append(Sy)

                if Sx == mode:
                    clustering.append(Sy)
                else:
                    clustering.append(Sx)
        for j in remove_data:
            for i in data_:
                if i[1] < 0.8:
                    break
                if j in i[0]:
                    remove.append(i)
        for i in remove:
            if i in data_:
                data_.remove(i)

        ret[mode] = clustering
        with open("ret.json","a",encoding="utf-8") as f:
            f.write(f"参考数据：\n{mode}\n")
            f.write("*"*50 + "\n")
            f.write(f"{mode}\n")
            sentences.remove(mode)
            for i in clustering:
                f.write(f"{i}\n")
                sentences.remove(i)
        print(ret)
        n_ += 1
    with open("ret.json","a",encoding="utf-8") as f:
        f.write("参考数据\nother\n")
        f.write("*" * 50 + "\n")
        for i in sentences:
            f.write(i + "\n")
