#include <dlib/image_processing/frontal_face_detector.h>
#include <dlib/image_processing/render_face_detections.h>
#include <dlib/image_processing.h>
#include <dlib/gui_widgets.h>
#include <dlib/image_io.h>
#include <iostream>

int main()
{
	//定义显示窗口
	dlib::image_window win, win_faces;
	//定义检测器
	dlib::frontal_face_detector detector = dlib::get_frontal_face_detector();
	//定义数据输入sp
	dlib::shape_predictor sp;
	dlib::deserialize("shape_predictor_68_face_landmarks.dat") >> sp;
	//定义图像格式，与opencv不同
	dlib::array2d<dlib::rgb_pixel> img;
	//载入图像
	dlib::load_image(img, "test.jpg");
	//你可以使用下行pyramid_up来放大图像检测更小的脸
	//dlib::pyramid_up(img);
	std::vector<dlib::rectangle> dets = detector(img);
	std::vector<dlib::full_object_detection> shapes;
	//dets.size表示人脸数
	for (unsigned long j = 0; j < dets.size(); ++j)
	{
		dlib::full_object_detection shape = sp(img, dets[j]);
		std::cout << "number of parts: " << shape.num_parts() << std::endl;
		std::cout << "pixel position of first part:  " << shape.part(0) << std::endl;
		std::cout << "pixel position of second part: " << shape.part(1) << std::endl;
		// You get the idea, you can get all the face part locations if
		// you want them.  Here we just store them in shapes so we can
		// put them on the screen.
		shapes.push_back(shape);
	}
	//清除覆盖
	win.clear_overlay();
	//显示图像
	win.set_image(img);
	win.add_overlay(render_face_detections(shapes));

	dlib::array<dlib::array2d<dlib::rgb_pixel> > face_chips;
	extract_image_chips(img, get_face_chip_details(shapes), face_chips);
	//显示脸部，小图
	win_faces.set_image(tile_images(face_chips));
	win_faces.wait_until_closed();
}