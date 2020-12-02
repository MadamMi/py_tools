结构说明：xml里面记录了所有视频的信息。为了方便复盘和后续使用，将xml示例一并上传
实现的功能：将对应视频按照3000ms一个片段截取出来，
并将每个片段对应的xml信息解析，xml信息直接写到视频转化的每一帧中。
xml里面记录了所有视频的信息。

xml_root:xml文件的路径
video_path：存放videos的文件夹路径
save_path:存放解析后的videos（所有video按照3000ms为一个短视频进行截取，
		  每个短视频放到一个文件夹下。文件夹下的短视频截取成一帧一帧的图像形式）的文件夹路径
video_ids：待解析的视频名字，list或者all。all视频文件夹下表示所有视频文件都要解析
read_video函数：将待解析的视频按照3000ms解析出来
short_videos_path：存放截取成一帧一帧的图像的短视频文件路径
xml_reload：解析xml，并将短视频对应的xml信息写到图像中

生成和解析xml.py中：
write_xml(path)：生成xml文件。生成的文件见1.xml
test_xml(path):解析xml文件