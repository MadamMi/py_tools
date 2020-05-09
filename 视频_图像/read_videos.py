# coding:utf-8
import cv2
import os
import shutil


def video2imgs(video_path, savename, period=3000):
    each_image_time = 1000/30
    print(each_image_time)
    cur_time = 0
    start_time = 0
    count = 0

    videopathdir = os.listdir(video_path)

    for videodir in videopathdir:
        if videodir == 'NORM0049.MP4':
        # if videodir[-4:] == '.MP4':
            cur_time = 0
            start_time = 0
            savenameindex = 0
            listpath = os.path.join(savename, videodir[:-4])
            if not os.path.exists(listpath):
                os.mkdir(listpath)
            ot_path = os.path.join(listpath, str(count))
            if not os.path.exists(ot_path):
                os.mkdir(ot_path)
            videoCapture = cv2.VideoCapture(os.path.join(video_path, videodir))
            success, frame = videoCapture.read()
            while success:
                lastsavename = os.path.join(ot_path, str(savenameindex) + ".jpg")
                # frame = cv2.resize(frame, (768, 432))
                cv2.imwrite(lastsavename, frame)
                # frame90 = np.rot90(frame)
                # frame90 = np.rot90(frame90)
                # frame90 = np.rot90(frame90)

                # frame90 = cv2.resize(frame, (1280, 720))
                #if savenameindex % 30 == 0:
                cur_time += each_image_time
                if (cur_time - start_time) > period:
                    count += 1
                    start_time = cur_time
                    ot_path = os.path.join(listpath, str(count))
                    if not os.path.exists(ot_path):
                        os.mkdir(ot_path)
                    # image = cv2.resize(frame, (frame.shape[1]//2, frame.shape[0]//2))

                success, frame = videoCapture.read()  # 获取下一帧
                savenameindex = savenameindex + 1


def imgs2video(imgs_dir, save_path):
    fourcc = cv2.VideoWriter_fourcc('F', 'M', 'P', '4')

    fps = 30
    videoname = os.path.join(save_path, 'result.mp4')
    videoWriter = cv2.VideoWriter(videoname, fourcc, fps, (960, 540))
    imglists = os.listdir(save_path)

    for inx, imglist in enumerate(imglists):
        imagepath = os.path.join(save_path, imglist)
        image = cv2.imread(imagepath)
        videoWriter.write(image)
    videoWriter.release()


if __name__ == '__main__':
    savename = 'E:/work/videoCut/20200416'
    video_path = 'E:/work/videoCut/two_data_0416'
    save_path = 'E:/work/videoCut/20200408/test_scene'

    video2imgs(video_path, savename)
    # imgs2video(savename, save_path)

