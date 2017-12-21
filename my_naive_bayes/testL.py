
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
    mean1 = meanandstd1[0]
    std1 = meanandstd1[1]
    mean0 =meanandstd0[0]
    std0 = meanandstd0[1]
    m, n = new_array.shape
    # print(m,n) 240*320
    for i in range(m):
        for j in range(n):
            if new_array[i][j] == 0:
                new_array[i][j]=0
            else:
                new_array[i][j] = calculate_fishdata(new_array[i][j],probability1,probability0,mean0,std0,mean1,std1)
    return new_array


def calculate_fishdata(data,probability1,probability0,mean0,std0,mean1,std1):
    normal_data = data/255
    probability_1 = float(probability1*(1/(math.sqrt(std1*std1*2*math.pi))*math.exp(-((normal_data-mean1)*(normal_data-mean1))/(2*std1*std1))))
    probability_0 = float(probability0*(1/(math.sqrt(std0*std0*2*math.pi))*math.exp(-((normal_data-mean0)*(normal_data-mean0))/(2*std0*std0))))
    if probability_1 > probability_0:
        normal_data = 20
    else:
        normal_data = 180
    return normal_data


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



# def getgray(data):
#     m,n = data.shape
#     for i in range(m):
#         if data[i][4] ==1:
#             data[i][0] =0
#         else:
#             data[i][0] = 255
#     mydata = data[:, 0]
#
#     return mydata
#
# def coloring(data):
#     plt.imshow(data)
#     fig =plt.figure()
#     ax = fig.add_subplot(1,1,1)
#     ax.imshow(im2,cmap='gray')
#     plt.show()

# a = [[1,2],[3,4]]
# b = np.array(a)
# c= b
# d =b.copy()
# print(id(b))
# print(id(c))
# print(id(d))

# im = Image.open('fish1.jpg')
# # im.show()
# im1 = im.convert('L')
# im1.show()
# img = np.array(im1)
#
# print(img.shape)
# print(img)
# print(img[10][50])
# im2 = 255-img
# # plt.imshow(im2)
# fig =plt.figure()
# ax = fig.add_subplot(1,1,1)
# ax.imshow(im2,cmap='gray')
# plt.show()


