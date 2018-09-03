import csv
import numpy as np
import math


class fish():
    def __init__(self):
        pass

    def loaddata(self,filename):
        with open(filename,'r') as csvfile:
            lines = csv.reader(csvfile)
            dataset = list(lines)
            # print(len(dataset)) 一共7696个数据点，每个数据点是5维的
            data = np.array(dataset,dtype=float)
            # print(data.shape) 观察矩阵的维数
            # print(data.size)  观察矩阵的大小，即一共有多少个数据
            return data

    def calculate_mean_std(self,array):
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

    def calculate_probability(self,array):
        # 创建测试集，便于计算正确率
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
        meanandstd1 = self.calculate_mean_std(yes_data)
        meanandstd0 = self.calculate_mean_std(no_data)
        mean1 = meanandstd1[0]
        std1 = meanandstd1[1]
        mean0 =meanandstd0[0]
        std0 = meanandstd0[1]
        print(mean1,std1,mean0,std0)
        for i in range(m):
            data_probability1 = float(probability1*(1/(math.sqrt(std1*std1*2*math.pi))*math.exp(-((array[i][0]-mean1)*(array[i][0]-mean1))/(2*std1*std1))))
            data_probability_not = float(probability0*(1/(math.sqrt(std0*std0*2*math.pi))*math.exp(-((array[i][0]-mean0)*(array[i][0]-mean0))/(2*std0*std0))))
            if data_probability1 > data_probability_not:
                testdata_set[i][4]=1
            else:
                testdata_set[i][4] = -1
        return testdata_set
    # 获取预测的准确率

    def getAccuracy(self,testSet,array):
        correct = 0
        m,n = testSet.shape
        for x in range(m):
            if testSet[x][4] == array[x][4]:
                    correct +=1
        print('共有{}个数据预测正确，共有{}个测试数据'.format(correct, m))
        return (correct/float(m))*100.0

    def run(self):
        data = self.loaddata('fishdata2.txt')
        test_set = self.calculate_probability(data)
        accuracy = self.getAccuracy(test_set, data)
        print('准确率为：' + repr(accuracy) + '%')

# def imageColor():


if __name__ == '__main__':
     a = fish()
     a.run()



