import csv
import numpy as np
import math


def loaddata(filename):
    with open(filename,'r') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        # print(len(dataset)) 一共7696个数据点，每个数据点是5维的
        data = np.array(dataset,dtype=float)
        # print(data.shape) 观察矩阵的维数
        # print(data.size)  观察矩阵的大小，即一共有多少个数据
        return data


def calculate_mean_std(array):
    m,n = array.shape
    meanandstdlist = []
    for j in range(n-1):
        features = array[:, j]
        # print(features)
        # print(len(features))
        meanValuej = np.mean(features,axis=0)
        stdj = np.std(features,axis=0)
        meanandstdlist.append(meanValuej)
        meanandstdlist.append(stdj)
    # print(meanandstdlist)
    return  meanandstdlist


def calculate_probability(array):
    # 创建测试集的复制版本，便于计算正确率
    testdata_set =array.copy()
    m, n = array.shape
    feature_classfication = array[:, 4]
    # 找出为1 的个数
    counts_1 = np.sum(feature_classfication == 1)
    # print(counts_1)
    # 找出为-1 的个数
    counts_not = np.sum(feature_classfication == -1)
    # 分割数组，分为为1 的和为-1 的
    yes_data = array[0:counts_1, :]
    no_data = array[counts_1:, :]
    # print(yes_data.shape)
    # print(no_data.shape)
    probability1 = float(counts_1 / m)
    probability0 = float(counts_not / m)
    # 分别计算链各个数组的均值和方差
    meanandstd1 = calculate_mean_std(yes_data)
    meanandstd0 = calculate_mean_std(no_data)
    mean1_R = meanandstd1[2]
    std1_R = meanandstd1[3]
    mean1_G = meanandstd1[4]
    std1_G = meanandstd1[5]
    mean1_B = meanandstd1[6]
    std1_B = meanandstd1[7]
    mean0_R =meanandstd0[2]
    std0_R = meanandstd0[3]
    mean0_G = meanandstd0[4]
    std0_G = meanandstd0[5]
    mean0_B = meanandstd0[6]
    std0_B = meanandstd0[7]
    print(meanandstd1,meanandstd0)
    for i in range(m):
        data_probability1_R = float((1/(math.sqrt(std1_R*std1_R*2*math.pi))*math.exp(-((array[i][1]-mean1_R)*(array[i][1]-mean1_R))/(2*std1_R*std1_R))))
        data_probability1_G = float((1/(math.sqrt(std1_G*std1_G*2*math.pi))*math.exp(-((array[i][2]-mean1_G)*(array[i][2]-mean1_G))/(2*std1_G*std1_G))))
        data_probability1_B = float((1/(math.sqrt(std1_B*std1_B*2*math.pi))*math.exp(-((array[i][3]-mean1_B)*(array[i][3]-mean1_B))/(2*std1_B*std1_B))))
        data_probability1 =float(probability1*data_probability1_R*data_probability1_G*data_probability1_B)
        data_probability0_not_R = float((1/(math.sqrt(std0_R*std0_R*2*math.pi))*math.exp(-((array[i][1]-mean0_R)*(array[i][1]-mean0_R))/(2*std0_R*std0_R))))
        data_probability0_not_G = float((1/(math.sqrt(std0_G*std0_G*2*math.pi))*math.exp(-((array[i][2]-mean0_G)*(array[i][2]-mean1_G))/(2*std0_G*std0_G))))
        data_probability0_not_B = float((1/(math.sqrt(std0_B*std0_B*2*math.pi))*math.exp(-((array[i][3]-mean0_B)*(array[i][3]-mean1_B))/(2*std0_G*std0_B))))
        data_probability0_not = float(probability0*data_probability0_not_R*data_probability0_not_G*data_probability0_not_B)
        if data_probability1 > data_probability0_not:
            testdata_set[i][4]=1
        else:
            testdata_set[i][4] = -1
    return testdata_set

# 获取测试集预测的准确率


def getAccuracy(testSet,array):
    correct = 0
    m,n = testSet.shape
    for x in range(m):
        if testSet[x][4] == array[x][4]:
                correct +=1
    print('共有{}个数据预测正确，共有{}个测试数据'.format(correct, m))
    return (correct/float(m))*100.0


if __name__ == '__main__':
     data = loaddata('fishdata2.txt')
     test_set = calculate_probability(data)
     accuracy = getAccuracy(test_set, data)
     print('准确率为：' + repr(accuracy) + '%')
