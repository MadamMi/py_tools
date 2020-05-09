# coding:utf-8
import os
import hashlib
import sys
import cv2
import numpy as np


def delete_empty_image(dir_path):
    EXT = ['.jpg', '.jpeg']
    img_files = [os.path.join(rootdir, file) for rootdir, _, files in os.walk(dir_path) for file in files if
                 (os.path.splitext(file)[-1] in EXT)]
    for curr, file in enumerate(img_files):
        #file = 'H:/datasets_khy/scene_classification/find_imgs/00033.jpg'
        try:
            img = cv2.imdecode(np.fromfile(file, dtype=np.uint8), -1)
            image = cv2.imread(np.fromfile(file, dtype=np.uint8), -1)
            if (img is None) or ((image.shape[0] < 50) or (image.shape[1] < 50)):
                print("rm the path:{}".format(file))
                os.remove(file)
            elif (image.shape[0] < 50) or (image.shape[1] < 50):
                print("rm the path:{}".format(file))
                os.remove(file)
            elif image.shape[2] < 3:
                print("rm the path:{}".format(file))
                os.remove(file)
            else:
                pass
        except:
            #os.remove(file)
            continue


def getmd5(filename):
    file_txt = open(filename, 'rb').read()
    m = hashlib.md5(file_txt)
    return m.hexdigest()


def main(path):
    all_size = {}
    total_file = 0
    total_delete = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            real_path = os.path.join(root, file)
            total_file += 1
            if os.path.isfile(real_path):
                size = os.stat(real_path).st_size
                name_and_md5 = [real_path, '']
                if size in all_size.keys():
                    new_md5 = getmd5(real_path)
                    import pdb
                    # pdb.set_trace()
                    if all_size[size][1] == '':
                        all_size[size][1] = getmd5(all_size[size][0])
                    if new_md5 in all_size[size]:
                        os.remove(real_path)
                        print('删除', file)
                        total_delete += 1
                    else:
                        all_size[size].append(new_md5)
                else:
                    all_size[size] = name_and_md5
    print('文件个数：', total_file)
    print('删除个数：', total_delete)


if __name__ == '__main__':
    path = sys.argv[1]
    delete_empty_image(path)
    main(path)