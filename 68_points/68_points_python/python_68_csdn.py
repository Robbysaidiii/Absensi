import dlib                  #人脸识别的库dlib
import numpy as np    #数据处理的库numpy
import cv2                   #图像处理的库OpenCv

#dlib预测器
detector = dlib.get_frontal_face_detector()
#读入68点数据
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

 #cv2读取图像
img=cv2.imread("test.jpg")
#设置字体
font = cv2.FONT_HERSHEY_SIMPLEX
 
# 取灰度
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
 
# 人脸数rects
rects = detector(img_gray, 0)
 
for i in range(len(rects)):
    #获取点矩阵68*2
    landmarks = np.matrix([[p.x, p.y] for p in predictor(img, rects[i]).parts()])
    for idx, point in enumerate(landmarks):
        # 68点的坐标
        pos = (point[0, 0], point[0, 1])
        # 利用cv2.circle给每个特征点画一个点，共68个
        cv2.circle(img, pos, 1, (0, 0, 255), -1)

        #避免数字标签与68点重合，坐标微微移动
        pos = list(pos)
        pos[0] = pos[0] + 5
        pos[1] = pos[1] + 5
        pos = tuple(pos)
    
        #利用cv2.putText输出1-68
        cv2.putText(img, str(idx+1), pos, font, 0.3, (255, 0, 0), 1, cv2.LINE_AA)
 
cv2.namedWindow("python_68_points", 2)
cv2.imshow("python_68_points", img)
cv2.waitKey(0) 
