Img = imread("F:\68_points\68_points_matlab\test.jpg");
[bboxes,shapes]=face_landmarks(Img);
face=insertObjectAnnotation(Img,'rectangle',bboxes,'face');%Ìí¼Órectangle¿ò
faceLandmarks=insertMarker(face,shapes);                   %Ìí¼Ólandmarks
imshow(faceLandmarks);