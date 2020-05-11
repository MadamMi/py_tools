# coding:utf-8
import xml.etree.ElementTree as ElementTree
from xml.dom.minidom import parse
import cv2
import os
import shutil


# 将视频按照视频结构化的逻辑截取为短视频片段，并将片段的path和视频名字放入字典内
# video_ids表示想要截取的短视频。可以为列表，也可以为all. all表示文件夹下所有的视频文件都做解析
def read_video(video_path, save_path, video_ids, period=3000):
    each_image_time = 1000/30  # 视频的帧率为一秒30帧
    videopathdir = os.listdir(video_path)
    if video_ids == 'all':
        video_ids = videopathdir

    for videodir in video_ids:
        # if videodir == 'NORM0049.MP4':
        if videodir[-4:] == '.MP4':
            count = 0
            cur_time = 0
            start_time = 0
            savenameindex = 0
            listpath = os.path.join(save_path, videodir[:-4])

            if not os.path.exists(listpath):
                os.mkdir(listpath)
            ot_path = os.path.join(listpath, str(count))
            if not os.path.exists(ot_path):
                os.mkdir(ot_path)
            videoCapture = cv2.VideoCapture(os.path.join(video_path, videodir))
            success, frame = videoCapture.read()
            while success:
                lastsavename = os.path.join(ot_path, str(savenameindex) + ".jpg")
                frame = cv2.resize(frame, (768, 432))
                cv2.imwrite(lastsavename, frame)

                cur_time += each_image_time
                if (cur_time - start_time) > period:
                    count += 1
                    start_time = cur_time
                    ot_path = os.path.join(listpath, str(count))
                    if not os.path.exists(ot_path):
                        os.mkdir(ot_path)

                success, frame = videoCapture.read()  # 获取下一帧
                savenameindex = savenameindex + 1


# 解析xml并将其显示在对应的短视频内
def xml_reload(xml_path, video_ids, short_videos_path):
    # 开始解析xml文件
    doc = parse(xml_path)
    sum_root = doc.documentElement
    roots = sum_root.getElementsByTagName('file')
    for root in roots:
        file_name = root.getAttribute('name')
        if file_name[-12:] in video_ids:
            labels = root.getElementsByTagName('label')

            for inx, label in enumerate(labels):
                start_time = int(label.getAttribute('start_time'))
                end_time = int(label.getAttribute('end_time'))
                print("start time: ", start_time)
                print("end time: ", end_time)

                video_path = short_videos_path + '/' + str(inx)
                xml_video_path = short_videos_path + '/' + str(inx) + '_log'
                if not os.path.exists(xml_video_path):
                    os.mkdir(xml_video_path)

                label_tag = label.getElementsByTagName("tag")[0]
                # get emotion, bit(str)
                emotion = int(label_tag.getAttribute('emotion'))
                emotion = bin(emotion).replace('0b', '')
                emotion = str(emotion).rjust(28, '0')
                print("bit emotion : ", emotion)

                # get scene_class
                scene_class = label_tag.getAttribute('scene_class')
                print('scene class:', scene_class)

                # get face number
                face_num = label_tag.getAttribute('face_num')
                face_num = bin(int(face_num)).replace('0b', '')
                face_num = str(face_num).rjust(8, '0')
                print('face number : ', face_num)

                # get object detection
                object_detect = int(label_tag.getAttribute('object_detect'))
                object_detect = bin(object_detect).replace('0b', '')
                object_detect = str(object_detect).rjust(24, '0')
                print("object_detect : ", object_detect)

                # get ori face
                ori_face = int(label_tag.getAttribute('ori_face'))
                ori_face = bin(ori_face).replace('0b', '')
                ori_face = str(ori_face).rjust(16, '0')
                print("ori_face : ", ori_face)

                # get gender class
                gender_class = int(label_tag.getAttribute('gender_class'))
                gender_class = bin(gender_class).replace('0b', '')
                gender_class = str(gender_class).rjust(16, '0')
                print("gender_class : ", gender_class)

                # get face forward
                label_tag_forward = label_tag.getElementsByTagName("face_forward_time")
                count_forward = len(label_tag_forward)
                print("forward time: ", count_forward)

                # get face happy
                label_tag_happy = label_tag.getElementsByTagName("face_happy_time")
                count_happy = len(label_tag_happy)
                print("happy time: ", count_happy)

                # get pet close-up time
                label_pet_close = label_tag.getElementsByTagName("pet_closeup")
                count_pet_close = len(label_pet_close)
                print("pet closeup time: ", count_pet_close)

                img_lists = os.listdir(video_path)
                for index, img_list in enumerate(img_lists):
                    img_path = video_path + '/' + img_list
                    frame = cv2.imread(img_path)

                    text1 = "object:" + object_detect
                    cv2.putText(frame, text1, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 200, 0), 1)

                    text2 = "scene:" + scene_class
                    cv2.putText(frame, text2, (50, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 200, 0), 1)

                    text3 = "emotion:" + emotion
                    cv2.putText(frame, text3, (50, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 200, 0), 1)

                    text4 = "forward:" + ori_face
                    cv2.putText(frame, text4, (50, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 200, 0), 1)

                    text5 = "facenum:" + face_num + "happytime:" + str(count_happy)
                    text6 = 'forwardtime:' + str(count_forward) + 'pettime:' + str(count_pet_close)
                    cv2.putText(frame, text5, (50, 250), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 200, 0), 1)
                    cv2.putText(frame, text6, (50, 300), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 200, 0), 1)
                    savepath = xml_video_path + '/' + str(index)+'.jpg'
                    cv2.imwrite(savepath, frame)


def copy_img():
    root = "F:/share/test_data/2/"
    imgroot = "F:/share/test_data/2/139.jpg"
    for i in range(30):
        newroot = root + str(i)+'.jpg'
        shutil.copyfile(imgroot, newroot)


xml_root = 'E:/work/videoCut/test_data/two_data_0416/20200430.xml'
video_path = 'E:/work/videoCut/test_data/two_data_0416'
save_path = 'E:/work/videoCut/test_data/20200416'
video_ids = ['SLOW0002.MP4']
read_video(video_path, save_path, video_ids, period=3000)
short_videos_path = 'E:/work/videoCut/test_data/20200416/SLOW0002'
xml_reload(xml_root, video_ids, short_videos_path)
