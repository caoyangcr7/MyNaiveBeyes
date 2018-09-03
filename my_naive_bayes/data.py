from sklearn import datasets,cross_validation,naive_bayes
import numpy as np
import  matplotlib.pyplot as plt


def show_digits():
    # 加载8X8的手写数字位图
    digits = datasets.load_digits()
    fig = plt.figure()
    # 输出第一张图片的向量
    print('vector from images 0 ',digits.data[0])
    for i in range(25):
        ax = fig.add_subplot(5,5,i+1)
        ax.imshow(digits.images[i],interpolation='nearest' )
    plt.show()


if __name__ =='__main__':
    show_digits()