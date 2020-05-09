import cv2
import os
import shutil


def crop_methods(image, size):
    try:
        h, w = image.shape[0], image.shape[1]
        crop_image = image[size:h-size, size:w-size]
        return crop_image
    except:
        pass
        return None


def crop_method2(image, ratio):
    try:
        h, w = image.shape[0], image.shape[1]
        crop_image = image[int(h*ratio):h-int(h*ratio), int(w*ratio):w-int(w*ratio)]
        return crop_image
    except:
        pass
        return None


if __name__ == '__main__':
    root = 'F:/web_data/sougou2'
    saveroot = 'F:/web_data/crop/'
    data_lists = os.listdir(root)
    count = 1764
    for inx, data_list in enumerate(data_lists):
        image_path = os.path.join(root, data_list)
        print(image_path)
        image = cv2.imread(image_path)
        os.remove(image_path)
        crop_img = crop_method2(image, 0.1)
        savepath = saveroot + str(count)+'.jpg'
        cv2.imwrite(savepath, crop_img)
        count += 1


