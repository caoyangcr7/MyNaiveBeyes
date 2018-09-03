import numpy as np
import math
import matplotlib.pyplot as plt
from  fishL import fish

predict_list = []
a = fish()
def getdata(filename):
    # a = fish()
    original_data = a.loaddata(filename) # 此处filenam为'fishdata2.txt'
    L_data = original_data[:, 0:1]
    # print(L_data.shape)
    return L_data


def e_step(L_array,k,first_list):
    # first_list 为first_u1, first_sigma1,a1,    first_u2, first_sigma2,a2
    expectations =[]
    m,n = L_array.shape
    for i in range(m):
        tmplist =[]
        denom = 0
        for j in range(k):
            denom += float(first_list[j][2]*(1/(math.sqrt((2*math.pi*first_list[j][1])))*(math.exp((-1 / (2 * (float(first_list[j][1]))))
                              * (float(L_array[i][0] - first_list[j][0])) ** 2))))
        for j in range(k):
            numer = float(first_list[j][2]*(1/(math.sqrt((2*math.pi*first_list[j][1])))*(math.exp((-1 / (2 * (float(first_list[j][1]))))
                              * (float(L_array[i][0] - first_list[j][0])) ** 2))))
            # 计算模型K对观测数据Xi的响应概率
            yjk = numer/denom
            tmplist.append(float(yjk))
        expectations.append(tmplist)
     # expectations 应该是一个j*2的列表
    return expectations


def m_step(L_array,expect,m,k):
    # 使用全局变量 predict_list
    global predict_list
    predict_list_tmp = []
    for j in range(k):
        templist = []
        numer1 = 0
        denom1 = 0
        numer2= 0
        denom2 = 0
        numer3 = 0
        denom3 =0
        for i in range(m):
              numer1 += float(expect[i][j]*L_array[i][0])
              denom1 += float(expect[i][j])
        temp_data1 = numer1/denom1
        templist.append(float(temp_data1))
        for i in range(m):
            numer2 += expect[i][j]*((L_array[i][0]-templist[0])**2)
            denom2 += expect[i][j]
        temp_data2 =numer2/denom2
        templist.append(temp_data2)
        for i in range(m):
            numer3 += expect[i][j]
        temp_data3 = numer3/m
        templist.append(temp_data3)
        predict_list_tmp.append(templist)
        predict_list =predict_list_tmp
    return predict_list
    # predict_list 应该是[[均值1,方差1,a1],[均值2,方差2,a2]]的形式


def run(iter_num,first_predict_list, Epsilon):
    global predict_list
    data_array = getdata('fishdata2.txt')
    # 实际的均值和均方差 [0.425659401596 0.10651220886 ，0.728790320724 0.15768537414]
    print('开始迭代')
    for i in range(iter_num):
        if i == 0:
            old_argument = first_predict_list.copy()
            expectations = e_step(data_array, 2, first_predict_list)
            new_predict = m_step(data_array, expectations, 7696, 2)
            print(i, new_predict)
            new_predict = np.array(new_predict)
            old_predict = np.array(old_argument)
            if float(abs((new_predict - old_predict).any())) < Epsilon:
                return new_predict
            else:
                print('continue')
        else:
            old_argument = predict_list.copy()
            expectations = e_step(data_array,2,predict_list)
            new_predict= m_step(data_array,expectations,7696,2)
            new_predict = np.array(new_predict)
            old_predict = np.array(old_argument)
            print(i,new_predict,old_predict)
            if float(((new_predict - old_predict).max())) < Epsilon:
                return new_predict
            else:
                print('continue')
    print('the iter_num {} is not big enough'.format(iter_num))


def calculate_pro(data,new_predict):
    normal_data = data / 255
    probability_1 = float(new_predict[0][2]* (1 / (math.sqrt(new_predict[0][1] * 2 * math.pi)) * math.exp(
        -((normal_data - new_predict[0][0]) * (normal_data - new_predict[0][0])) / (2 * new_predict[0][1]))))
    probability_0 = float(new_predict[1][2] * (1 / (math.sqrt(new_predict[1][1] * 2 * math.pi)) * math.exp(
        -((normal_data - new_predict[1][0]) * (normal_data - new_predict[1][0])) / (2 * new_predict[1][1]))))
    print(probability_1,probability_0)
    if probability_1 > probability_0:
        normal_data = 20
    else:
        normal_data = 180
    return normal_data


def color_fish(new_array,predict):
    m, n = new_array.shape
    # print(m,n) 240*320
    for i in range(m):
        for j in range(n):
            if new_array[i][j] == 0:
                new_array[i][j] = 0
            else:
                new_array[i][j] = calculate_pro(new_array[i][j],predict )
    return new_array


def show_image(prediction_array):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(2, 1, 1)
    ax.set_title('original_image')
    # c = fish()
    ax.imshow(a.loaddata('fishdata3.txt'),cmap='gray')
    ax = fig.add_subplot(2, 1, 2)
    ax.set_title('prediction_image')
    ax.imshow(prediction_array,cmap='gray')
    plt.show()

if __name__ == '__main__':
    # b = fish()
    original_data = a.loaddata('fishdata3.txt')
    predict_mean_std = run(100,[[0.3,0.05,0.6],[0.75,0.04,0.4]],0.0001)
    new_array = color_fish(original_data,predict_mean_std)
    show_image(new_array)









