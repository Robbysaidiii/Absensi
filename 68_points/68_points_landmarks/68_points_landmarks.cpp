/******************************************/
/*欢迎关注CSDN博主Deephao  ID：qq_39567427*/
/*只声明dilb空间不声明cv空间，因为两个空间*/
/**********具有同名函数，防止混淆**********/

#include <dlib\opencv.h>
#include <opencv2\opencv.hpp>
#include <dlib\image_processing\frontal_face_detector.h>
#include <dlib\image_processing\render_face_detections.h>
#include <dlib\image_processing.h>
#include <dlib\gui_widgets.h>

//声明dlib名称空间
using namespace dlib;

//声明std名称空间
using namespace std;

int main() {
	//加载检测器
	frontal_face_detector detector = get_frontal_face_detector();
	shape_predictor sp;
	//将文件中的模型放置再sp中
	deserialize("shape_predictor_68_face_landmarks.dat") >> sp;
	cv::Mat img;
	//读取图片
	img = cv::imread("test.jpg");
	//将其转化为RGB像素图片
	cv_image<bgr_pixel> cimg(img);
	//开始进行脸部识别
	std::vector<rectangle> faces = detector(cimg);
	//发现每一个脸的pos估计 Find the pose of each face
	std::vector<full_object_detection> shapes;
	//确定脸部的数量
	unsigned faceNumber = faces.size();
	//将所有脸的区域放入集合之中
	for (unsigned i = 0; i < faceNumber; i++)
		shapes.push_back(sp(cimg, faces[i]));
	if (!shapes.empty()) {
		int faceNumber = shapes.size();
		for (int j = 0; j < faceNumber; j++)
		{
			for (int i = 0; i < 68; i++)
			{
				//用来画特征值的点
				cv::circle(img, cvPoint(shapes[j].part(i).x(), shapes[j].part(i).y()), 3, cv::Scalar(0, 0, 255), -1);
				//显示特征点数字
				cv::putText(img, to_string(i), cvPoint(shapes[0].part(i).x() + 5, shapes[0].part(i).y() + 5), cv::FONT_HERSHEY_COMPLEX, 0.2, cv::Scalar(255, 0, 0));

			}
		}
	}
	//显示图片
	cv::namedWindow("68_points_landmarks", cv::WINDOW_AUTOSIZE);
	cv::imshow("68_points_landmarks", img);
	cv::waitKey(0);
}