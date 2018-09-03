from fishL import fish
import numpy as np


# a= [[1,2],[3,4],[5,6]]
# b =np.array(a)
# c =a.copy()
# print(c)
# print(b[2,1])
# print(b[2][1])
# c= b[0:2,:]
# print(c)
# d = b[:,0:1]
# print(d)
# e= b[1:,:]
# print(e)

# a = [[1,2,3]]
# b =np.array(a)
# # print(np.linalg.inv(b))
# print(b.T)

# b = np.array(a)
# print(np.cov(b))
# print(b.std())
# print(b.mean())

# c = []
# c.append(1)
# c.append(b)
# print(c)
# print(c[1][1][0])

# a =np.array([1,2,3])
# alist =[]
# blist = []
# clist =[]
# a = np.array([[1,0,1],[0,1,2],[2,3,4]])
# b = np.array([[1,0,1],[0,1,2],[2,3,4]])
# c = np.array([[0.5,0,1],[2,3,4],[3,4,5]])
# d = np.array([[0.5,0,1],[2,3,4],[3,4,5]])
# alist.append(a)
# alist.append(b)
# blist.append(c)
# blist.append(d)
# clist.append(alist)
# clist.append(blist)
# print((clist[1][1]-clist[0][1]))
# print((alist[1]-blist[1]).max())
# print(alist-blist)
# print((b-c).max())



#
# def getdata(filename):
#     a = fish()
#     original_data = a.loaddata(filename) # 此处filenam为'fishdata2.txt'
#     feature_classfication = original_data[:, 4]
#     counts_1 = np.sum(feature_classfication == 1)
#     # print(counts_1)
#     # 找出为-1 的个数
#     counts_not = np.sum(feature_classfication == -1)
#     # 分割数组，分为为1 的和为-1 的
#     RGB_data = original_data[:, 1:4]
#     yes_data = original_data[0:counts_1,1:4]
#     no_data = original_data[counts_1:, 1:4]
#     # print(L_data.shape)
#     yes_data_T = yes_data.T
#     no_data_T = no_data.T
#     print(np.cov(yes_data_T),np.cov(no_data_T))
#     # [[ 0.0292778   0.01255938  0.0027168 ]
#     # [ 0.01255938  0.00902525  0.0065936 ]
#     # [ 0.0027168   0.0065936   0.01111143]]
#     # [[ 0.01696328  0.01833531  0.02183611]
#     # [ 0.01833531  0.02731825  0.03871635]
#     # [ 0.02183611  0.03871635  0.06444387]]
# getdata('fishdata2.txt')

# a = [[row for row in range(5)] for col in range(3)]
# b =np.array(a)
# print(b.shape)
# print(len(a))

# a=np.array([1,2,3])
# print(a)
# b = np.array([[1],[2],[3]])
# c= np.dot(a,b)
# print(c)
# d = c[0]
# print(d)
# print(type(d))

# a = np.array([[1,2],[3,4]])
# b = a[:,1:2]
# c =np.array([[1,2]])
# print(c.shape)
# print(b)
# print(b.shape)
# u2 = (np.array([[0.7,0.65,0.77]])).T
# print(u2)
#
# a= np.array([[1]])
# print((a)[0][0])
# print(type(a[0][0]))


# def cal():
#     a = [[ 0.0300775 ,  0.01260786,  0.00228922],
#        [ 0.01260786,  0.00670522,  0.00193607],
#        [ 0.00228922,  0.00193607,  0.00156885]]
#     b = np.linalg.inv(a)
#     print(b)
#     c = (np.dot(np.dot(((xj - new_predict[0][0]).T), np.linalg.inv(new_predict[0][1])),xj-new_predict[0][0]))[0][0])))))
# cal()

# xj = np.array([1,2,3])
# print(xj.shape)

# zeros_arr=np.zeros((2,3))
# print(zeros_arr)
# zeros_arr[0][0] = 1
# print(zeros_arr)