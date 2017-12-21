import numpy as np
import math
import matplotlib.pyplot as plt
from  fishL import fish

predict_list = []
a= fish()


def getdata(filename):
    original_data = a.loaddata(filename) # 此处filenam为'fishdata2.txt'
    RGB_data = original_data[:, 1:4]
    # 获取rgb矩阵的转置，便于求协方差矩阵
    RGB_data_T = RGB_data.T
    print(RGB_data_T.shape)
    # print(L_data.shape)
    return RGB_data_T


def e_step(RGB_array,k,first_list):
    # first_list为预测初值 内容应该是两种成分的均值向量，协方差矩阵，和成分的权重
    expectations =[]
    m,n = RGB_array.shape
    # print(np.dot(((RGB_array[:,3:4]-first_list[0][0]).T),np.linalg.inv(first_list[0][1])))
    for i in range(n):
        tmplist =[]
        denom = 0
        for j in range(k):
            denom += float(first_list[j][2]*(1/(2*math.pi*(math.sqrt(np.linalg.det(first_list[j][1])))))\
                     *(math.exp(-0.5*((np.dot(np.dot(((RGB_array[:,i:i+1]-first_list[j][0]).T),np.linalg.inv(first_list[j][1])),RGB_array[:,i:i+1]-first_list[j][0]))[0][0]))))
        for j in range(k):
            numer = float(first_list[j][2]*(1/(2*np.pi*(np.sqrt(np.linalg.det(first_list[j][1])))))
                          *(math.exp((-0.5 * ((np.dot(np.dot(((RGB_array[:, i:i+1] - first_list[j][0]).T), np.linalg.inv(first_list[j][1])),RGB_array[:,i:i+1]-first_list[j][0]))[0][0])))))
            # 计算模型K对观测数据Xi的响应概率
            yjk = numer/denom
            tmplist.append(float(yjk))
        expectations.append(tmplist)
     # expectations 应该是一个i*2的列表，7696*2的列表
    return expectations


def m_step(RGB_array,expect,n,k):
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
        for i in range(n):
              numer1 += (expect[i][j]*RGB_array[:,i:i+1])
              denom1 += float(expect[i][j])
        temp_data1 = numer1/denom1
        templist.append(temp_data1)
        for i in range(n):
            numer2 += expect[i][j]*((np.dot(RGB_array[:,i:i+1]-templist[0],(RGB_array[:,i:i+1]-templist[0]).T)))
            denom2 += expect[i][j]
        temp_data2 =numer2/denom2
        templist.append(temp_data2)
        for i in range(n):
            numer3 += expect[i][j]
        temp_data3 = numer3/n
        templist.append(temp_data3)
        predict_list_tmp.append(templist)
        predict_list =predict_list_tmp
    return predict_list
    # predict_list 应该是[[均值1,协方差矩阵1,a1],[均值2,协方差矩阵2,a2]]的形式


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
            # print(new_predict[1][1], old_argument[1][1])
            print(i, new_predict)
            # new_predict = np.array(new_predict)
            # old_predict = np.array(old_argument)
            if float((new_predict[0][1] - old_argument[0][1]).max()) < Epsilon:
                return new_predict
            else:
                print('continue')
        else:
            old_argument = predict_list.copy()
            expectations = e_step(data_array,2,predict_list)
            new_predict= m_step(data_array,expectations,7696,2)
            print(i,new_predict)
            # print(new_predict[1],old_argument[1])
            if (float(((new_predict[0][1] - old_argument[0][1]).max())) < Epsilon):
                return new_predict
            else:
                print('continue')
    print('the iter_num {} is not big enough'.format(iter_num))


def calculate_pro(new_predict,xj):
    probability_1 = float(new_predict[0][2]* (1/(2*math.pi*(np.sqrt(np.linalg.det(new_predict[0][1])))))
                          *(math.exp((-0.5 * ((np.dot(np.dot(((xj - new_predict[0][0]).T), np.linalg.inv(new_predict[0][1])),xj-new_predict[0][0]))[0][0])))))
    probability_0 = float(new_predict[1][2] * (1/(2*math.pi*(np.sqrt(np.linalg.det(new_predict[1][1])))))
                          * (math.exp((-0.5 * ((np.dot(np.dot(((xj - new_predict[1][0]).T),np.linalg.inv(new_predict[1][1])),xj-new_predict[1][0]))[0][0])))))
    # print(xj.shape)
    if probability_1 > probability_0:
        normal_data = 20
    else:
        normal_data = 180
    return normal_data

# def getXJ(dataR,dataG,dataB,i,j):
#     xj = (np.array([[dataR[i][j]],[dataG[i][j]],[dataB[i][j]]])).T
#     return xj


def color_fish(new_array,predict):
    dataR = getRGB('data_R.txt')
    dataG = getRGB('data_G.txt')
    dataB = getRGB('data_B.txt')
    print(dataR[120][130])
    m, n = new_array.shape
    # print(m,n) 240*320
    for i in range(m):
        for j in range(n):
            if new_array[i][j] == 0:
                new_array[i][j] = 0
            else:
                xj = (np.array([[dataR[i][j]], [dataG[i][j]], [dataB[i][j]]]))
                new_array[i][j] = calculate_pro(predict,xj )
    return new_array


def getRGB(rgb_file):
    rgb_data = a.loaddata(rgb_file)
    rgb_data = rgb_data/255
    return rgb_data

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
    # a = getRGB('data_R.txt')
    # print(np.argmax(a[120,:])) 120*130
    pre1_list = [row for row in range(3)]
    pre2_list =[row for row in range(3)]
    the_first_list = []
    u1 = (np.array([[0.6,0.4,0.3]])).T
    c1 = np.array([[ 0.0292778 ,0.01255938,0.0027168 ],[ 0.01255938,0.00902525,0.0065936],[0.0027168 ,0.0065936,0.01111143]])
    # [[ 0.0292778   0.01255938  0.0027168 ]
    # [ 0.01255938  0.00902525  0.0065936 ]
    #  [ 0.0027168   0.0065936   0.01111143]]
    d1 = 0.7
    pre1_list[0] = u1
    pre1_list[1] = c1
    pre1_list[2] = d1
    u2 = (np.array([[0.7,0.65,0.77]])).T
    # print(u2)
    # print(pre1_list)
    # print(pre1_list[0])
    c2 = np.array([[ 0.01696328,0.01833531,0.02183611],[0.01833531,0.02731825,0.03871635],[ 0.02183611,0.03871635,0.06444387]])
    #  # [[ 0.01696328  0.01833531  0.02183611]
#     # [ 0.01833531  0.02731825  0.03871635]
#     # [ 0.02183611  0.03871635  0.06444387]]
    d2 = 0.3
    pre2_list[0] = u2
    pre2_list[1] = c2
    pre2_list[2] = d2
    the_first_list.append(pre1_list)
    the_first_list.append(pre2_list)
    # print(the_first_list[0][0])
    # b = fish()
    original_data = a.loaddata('fishdata3.txt')
    predict_mean_std = run(100,the_first_list,0.0001)
    new_array = color_fish(original_data,predict_mean_std)
    show_image(new_array)

