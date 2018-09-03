import numpy as np
import matplotlib.pyplot as plt
import csv
from fishL import fish
import math


def loaddata(filename):
    with open(filename,'r') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        # print(dataset)
        # print(len(dataset)) # 一共7364个非0数据点
        data = np.array(dataset,dtype=float)
        # print(data.shape) # 观察矩阵的维数
        # print(data.size)  观察矩阵的大小，即一共有多少个数据
        return data


def color_fish(new_array):
    a = fish()
    old_array = loaddata('fishdata2.txt')
    k, l = old_array.shape
    feature_classfication = old_array[:, 4]
    counts_1 = np.sum(feature_classfication == 1)
    # print(counts_1)
    # 找出为-1 的个数
    counts_not = np.sum(feature_classfication == -1)
    probability1 = float(counts_1 / k)
    probability0 = float(counts_not /k )
    # print(probability0,probability1,k,l)
    yes_data = old_array[0:counts_1, :]
    no_data = old_array[counts_1:, :]
    meanandstd1 = a.calculate_mean_std(yes_data)
    meanandstd0 = a.calculate_mean_std(no_data)
    # print(meanandstd0,meanandstd1)
    # mean1_R = meanandstd1[2]
    # std1_R = meanandstd1[3]
    # mean1_G = meanandstd1[4]
    # std1_G = meanandstd1[5]
    # mean1_B = meanandstd1[6]
    # std1_B = meanandstd1[7]
    # mean0_R = meanandstd0[2]
    # std0_R = meanandstd0[3]
    # mean0_G = meanandstd0[4]
    # std0_G = meanandstd0[5]
    # mean0_B = meanandstd0[6]
    # std0_B = meanandstd0[7]
    rgb_R = getRGB('data_R.txt')
    rgb_G = getRGB('data_G.txt')
    rgb_B = getRGB('data_B.txt')
    mylist = []
    mean_std_list1 = list(meanandstd1)
    mean_std_list0 =list(meanandstd0)
    mylist.append(mean_std_list1)
    mylist.append(mean_std_list0)
    print(mylist)
    m, n = new_array.shape
    # print(m,n) 240*320
    for i in range(m):
        for j in range(n):
            if new_array[i][j] == 0:
                new_array[i][j]=0
            else:
                new_array[i][j] = calculate_fishdata(probability1,probability0,mylist,rgb_R,rgb_G,rgb_B,i,j)
    return new_array

def getRGB(rgb_file):
    rgb_data = loaddata(rgb_file)
    rgb_data = rgb_data/255
    return rgb_data


def calculate_fishdata(probability1,probability0,mean_std_list,rgbR,rgbG,rgbB,i,j):
    # normal_data = data/255
    probability1_R = float((1/(math.sqrt(mean_std_list[0][3]*mean_std_list[0][3]*2*math.pi))
                                            *math.exp(-((rgbR[i][j]-mean_std_list[0][2])
                                            *(rgbR[i][j]-mean_std_list[0][2]))/(2*mean_std_list[0][3]*mean_std_list[0][3]))))
    probability1_G = float((1/(math.sqrt(mean_std_list[0][5]*mean_std_list[0][5]*2*math.pi))
                                        *math.exp(-((rgbG[i][j]-mean_std_list[0][4])
                                        *(rgbG[i][j]-mean_std_list[0][4]))/(2*mean_std_list[0][5]*mean_std_list[0][5]))))
    probability1_B =float((1/(math.sqrt(mean_std_list[0][7]*mean_std_list[0][7]*2*math.pi))
                                        *math.exp(-((rgbG[i][j]-mean_std_list[0][6])
                                        *(rgbG[i][j]-mean_std_list[0][6]))/(2*mean_std_list[0][7]*mean_std_list[0][7]))))
    probability0_R = float((1/(math.sqrt(mean_std_list[1][3]*mean_std_list[1][3]*2*math.pi))
                                            *math.exp(-((rgbR[i][j]-mean_std_list[1][2])
                                            *(rgbR[i][j]-mean_std_list[1][2]))/(2*mean_std_list[1][3]*mean_std_list[1][3]))))
    probability0_G = float((1/(math.sqrt(mean_std_list[1][5]*mean_std_list[1][5]*2*math.pi))
                                        *math.exp(-((rgbG[i][j]-mean_std_list[1][4])
                                        *(rgbG[i][j]-mean_std_list[1][4]))/(2*mean_std_list[1][5]*mean_std_list[1][5]))))
    probability0_B= float((1/(math.sqrt(mean_std_list[1][5]*mean_std_list[1][5]*2*math.pi))
                                        *math.exp(-((rgbB[i][j]-mean_std_list[1][4])
                                        *(rgbB[i][j]-mean_std_list[1][4]))/(2*mean_std_list[1][5]*mean_std_list[1][5]))))
    probability_1 = float(probability1*probability1_R*probability1_G*probability1_B)
    probability_0 = float(probability0*probability0_R*probability0_G*probability0_B)
    if probability_1 > probability_0:
        dataij = 20
    else:
        dataij = 180
    return dataij


def show_image(prediction_array):
    fig =plt.figure(figsize=(8,8))
    ax = fig.add_subplot(2, 1, 1)
    ax.set_title('original_image')
    ax.imshow(loaddata('fishdata3.txt'), cmap='gray')
    ax = fig.add_subplot(2,1,2)
    ax.set_title('prediction_image')
    ax.imshow(prediction_array, cmap='gray')
    plt.show()

if __name__ =='__main__':
    im_array = loaddata('fishdata3.txt')
    prediction_array = color_fish(im_array)
    show_image(prediction_array)
