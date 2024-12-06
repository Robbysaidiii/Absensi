#include "dlib/matrix.h"
#include <dlib/image_processing/frontal_face_detector.h>
#include <dlib/image_processing/render_face_detections.h>
#include <dlib/image_processing.h>
#include <dlib/image_io.h>
#include "call_matlab.h"

using namespace dlib;
using namespace std;

void mex_function(
	const array2d<rgb_pixel >& img,
	matrix<double>& bboxes,
	matrix<double>& shape
)
{
	//开启检测模块
	frontal_face_detector detector = get_frontal_face_detector();

	//轮廓预测器
	shape_predictor sp;
	deserialize("shape_predictor_68_face_landmarks.dat") >> sp;

	//下面一行为放大图片来检测更小人脸，可以加上
	//pyramid_up(img);
	//人脸检测
	std::vector<dlib::rectangle> det = detector(img);
	std::vector<full_object_detection> shapes;

	//人脸数目
	int faces = det.size();
	bboxes = ones_matrix<double>(faces, 4);

	for (int i = 0; i < faces; i++)
	{
		bboxes(i,0)=det[i].left();
		bboxes(i,1)=det[i].top();
		bboxes(i,2)=det[i].width();
		bboxes(i,3)=det[i].height();
		shapes.push_back(sp(img, det[i]));
	}

	//一张图像中存在人脸个数
	cout << "Number of faces detected: " << faces << endl;

	int shape_colum = faces * 68;
	int k = 0;
	shape = ones_matrix<double>(shape_colum, 2);

	if (!shapes.empty())
	{
		for (int j = 0; j < faces; j++)
			for (int i = 0; i < 68; i++, k++)
			{
				shape(k, 0) = shapes[j].part(i).x();
				shape(k, 1) = shapes[j].part(i).y();
			}
	}
	cout << "finish!" << endl;
}
#include "mex_wrapper.cpp"