import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
sets = ['train', 'test', 'val']
classes = ['Mature fruit','Semimature fruit','Immature fruit']
def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)
def convert_annotation(image_id):
    in_file = open('data/Annotations/%s.xml' % (image_id), encoding='UTF-8')
    out_file = open('data/labels/%s.txt' % (image_id), 'w', encoding='UTF-8')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    if(size is None):
        return
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        print(obj)
        # difficult = float(object.find('difficult').text)
        cls = obj.find('name').text
        # if cls not in classes or int(difficult) == 1:
        #     continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        if(xmlbox is None):
            continue
        x1 = float(xmlbox.find('xmin').text)
        x2 = float(xmlbox.find('xmax').text)
        if x1>x2:
            t=x1
            x1=x2
            x2=t
        y1 = float(xmlbox.find('ymin').text)
        y2 = float(xmlbox.find('ymax').text)
        if y1>y2:
            t=y1
            y1=y2
            y2=t
        b = (x1, x2, y1, y2)
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    wd = getcwd()
    print(wd)
for image_set in sets:
    if not os.path.exists('data/labels/'):
        os.makedirs('data/labels/')
    image_ids = open('data/ImageSets/%s.txt' % (image_set),encoding="UTF-8").read().strip().split()
    list_file = open('data/%s.txt' % (image_set), 'w',encoding="UTF-8")
    for image_id in image_ids:
        list_file.write('data/images/%s.jpg\n' % (image_id))
        print(image_id)
        convert_annotation(image_id)
    list_file.close()
