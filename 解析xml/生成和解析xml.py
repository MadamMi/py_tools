# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

import torch
import SimpleITK as sitk
import cv2
import numpy as np
import copy
import shutil


def write_xml(path):
    root = ET.Element('annotation')  # 创建节点
    image = cv2.imread('F:/eye/images/'+path)
    h, w, c = image.shape
    print(image.shape)

    with open('F:/eye/'+path[0]+'.txt', 'r') as f:
        res = f.readlines()

    flag = res[0].strip()
    left_eye={}
    right_eye={}

    if flag == '1':
        left_eye['box'] = res[1].strip().split(',')
        left_eye['inner'] = res[2].strip().split(',')[:2]
        left_eye['outer'] = res[2].strip().split(',')[2:]
        left_eye['pupil'] = res[3].strip().split(',')[:3]
        left_eye['iris'] = res[3].strip().split(',')[3:]

    elif flag == '2':
        right_eye['box'] = res[1].strip().split(',')
        right_eye['inner'] = res[2].strip().split(',')[:2]
        right_eye['outer'] = res[2].strip().split(',')[2:]
        right_eye['pupil'] = res[3].strip().split(',')[:3]
        right_eye['iris'] = res[3].strip().split(',')[3:]

    elif flag == '3':
        left_eye['box'] = res[1].strip().split(',')
        left_eye['inner'] = res[2].strip().split(',')[:2]
        left_eye['outer'] = res[2].strip().split(',')[2:]
        left_eye['pupil'] = res[3].strip().split(',')[:3]
        left_eye['iris'] = res[3].strip().split(',')[3:]

        right_eye['box'] = res[4].strip().split(',')
        right_eye['inner'] = res[5].strip().split(',')[:2]
        right_eye['outer'] = res[5].strip().split(',')[2:]
        right_eye['pupil'] = res[6].strip().split(',')[:3]
        right_eye['iris'] = res[6].strip().split(',')[3:]

    if left_eye=={}:
        print('NULL')

    root = ET.Element('annotation')
    folder = ET.SubElement(root, 'folder')
    folder.text = 'images'

    filename = ET.SubElement(root, 'filename')
    filename.text = path

    size = ET.SubElement(root, 'size')
    width = ET.SubElement(size, 'width')
    width.text = str(w)

    height = ET.SubElement(size, 'height')
    height.text = str(h)

    depth = ET.SubElement(size, 'depth')
    depth.text = str(c)

    segmented = ET.SubElement(root, 'segmented')
    segmented.text = str(1)

    face = ET.SubElement(root, 'face')

    if not left_eye == {}:
        eye1 = ET.SubElement(face, 'eye')
        pose = ET.SubElement(eye1, 'pose')
        pose.text = 'Left'

        # eye box
        box = ET.SubElement(eye1, 'bndbox')
        xmin = ET.SubElement(box, 'xmin')
        xmin.text = left_eye['box'][0]

        ymin = ET.SubElement(box, 'ymin')
        ymin.text = left_eye['box'][1]

        xmax = ET.SubElement(box, 'xmax')
        xmax.text = str(int(left_eye['box'][0]) + int(left_eye['box'][2]))

        ymax = ET.SubElement(box, 'ymax')
        ymax.text = str(int(left_eye['box'][1]) + int(left_eye['box'][3]))

        # eye circle
        # pupil
        pupil = ET.SubElement(eye1, 'pupil')
        center = ET.SubElement(pupil, 'center')
        x = ET.SubElement(center, 'x')
        x.text = left_eye['pupil'][0]

        y = ET.SubElement(center, 'y')
        y.text = left_eye['pupil'][1]

        radius = ET.SubElement(pupil, 'radius')
        radius.text = left_eye['pupil'][2]

        # iris
        iris = ET.SubElement(eye1, 'iris')
        center2 = ET.SubElement(iris, 'center')
        x2 = ET.SubElement(center2, 'x')
        x2.text = left_eye['iris'][0]

        y2 = ET.SubElement(center2, 'y')
        y2.text = left_eye['iris'][1]

        radius2 = ET.SubElement(iris, 'radius')
        radius2.text = left_eye['iris'][2]

        # canthus
        canthus = ET.SubElement(eye1, 'canthus')
        point = ET.SubElement(canthus, 'point')
        x = ET.SubElement(point, 'x')
        x.text = left_eye['inner'][0]

        y = ET.SubElement(point, 'y')
        y.text = left_eye['inner'][1]

        location = ET.SubElement(point, 'location')
        location.text = 'inner'

        point2 = ET.SubElement(canthus, 'point')
        x2 = ET.SubElement(point2, 'x')
        x2.text = left_eye['outer'][0]

        y2 = ET.SubElement(point2, 'y')
        y2.text = left_eye['outer'][1]

        location2 = ET.SubElement(point2, 'location')
        location2.text = 'outer'

    if not right_eye == {}:
        eye2 = ET.SubElement(face, 'eye')
        pose2 = ET.SubElement(eye2, 'pose')
        pose2.text = 'right'

        # eye box
        box2 = ET.SubElement(eye2, 'bndbox')
        xmin2 = ET.SubElement(box2, 'xmin')
        xmin2.text = right_eye['box'][0]

        ymin2 = ET.SubElement(box2, 'ymin')
        ymin2.text = right_eye['box'][1]

        xmax2 = ET.SubElement(box2, 'xmax')
        xmax2.text = str(int(right_eye['box'][0]) + int(right_eye['box'][2]))

        ymax2 = ET.SubElement(box2, 'ymax')
        ymax2.text = str(int(right_eye['box'][1]) + int(right_eye['box'][3]))

        # eye circle
        # pupil
        pupil2 = ET.SubElement(eye2, 'pupil')
        center3 = ET.SubElement(pupil2, 'center')
        x3 = ET.SubElement(center3, 'x')
        x3.text = right_eye['pupil'][0]

        y3 = ET.SubElement(center3, 'y')
        y3.text = right_eye['pupil'][1]

        radius3 = ET.SubElement(pupil2, 'radius')
        radius3.text = right_eye['pupil'][2]

        # iris
        iris2 = ET.SubElement(eye2, 'iris')
        center4 = ET.SubElement(iris2, 'center')
        x4 = ET.SubElement(center4, 'x')
        x4.text = right_eye['iris'][0]

        y4 = ET.SubElement(center4, 'y')
        y4.text = right_eye['iris'][1]

        radius4 = ET.SubElement(iris2, 'radius')
        radius4.text = right_eye['iris'][2]

        # canthus
        canthus2 = ET.SubElement(eye2, 'canthus')
        point3 = ET.SubElement(canthus2, 'point')
        x5 = ET.SubElement(point3, 'x')
        x5.text = right_eye['inner'][0]

        y5 = ET.SubElement(point3, 'y')
        y5.text = right_eye['inner'][1]

        location3 = ET.SubElement(point3, 'location')
        location3.text = 'inner'

        point4 = ET.SubElement(canthus2, 'point')
        x6 = ET.SubElement(point4, 'x')
        x6.text = right_eye['outer'][0]

        y6 = ET.SubElement(point4, 'y')
        y6.text = right_eye['outer'][1]

        location4 = ET.SubElement(point4, 'location')
        location4.text = 'outer'


    tree = ET.ElementTree(root)
    tree.write('F:/eye/annotation/'+path[0]+'.xml')


def test_xml(path):
    image_path = 'F:/eye/images/' + path
    image = cv2.imread(image_path)

    xml_path = 'F:/eye/annotation/' + path[0] + '.xml'
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # faces = root.findall('face')
    for face in root.iter('face'):
        eyes = face.findall('eye')
        for eye in eyes:
            box = eye.find('bndbox')
            xmin = int(box.find('xmin').text)
            ymin = int(box.find('ymin').text)
            xmax = int(box.find('xmax').text)
            ymax = int(box.find('ymax').text)
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 1)

            pupil = eye.find('pupil')
            center = pupil.find('center')
            x = center.find('x').text
            y = center.find('y').text
            radius = pupil.find('radius').text
            cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 0), 1)

            iris = eye.find('iris')
            center = iris.find('center')
            x = center.find('x').text
            y = center.find('y').text
            radius = iris.find('radius').text
            cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 0), 1)

            canthus = eye.find('canthus')
            points = canthus.findall('point')
            for point in points:
                x = point.find('x').text
                y = point.find('y').text
                cv2.circle(image, (int(x), int(y)), 2, (0, 0, 255), 3)

    cv2.imshow('drow', image)
    cv2.waitKey()


if __name__ == '__main__':
    for i in range(1, 9):
        path = str(i)
        write_xml(path)