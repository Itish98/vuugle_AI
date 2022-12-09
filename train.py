import pixellib
import base64
from colorthief import ColorThief
import numpy as np
import glob
import os
from scipy.spatial import KDTree
import webcolors
import pandas as pd
from matplotlib import pyplot as plt
from webcolors import (
    CSS3_HEX_TO_NAMES,
    hex_to_rgb,
)
from pixellib.instance import instance_segmentation
from PIL import Image as im
from colorthief import ColorThief
def convert_rgb_to_names(rgb_tuple):
    
    # a dictionary of all the hex and their respective names in css3
    css3_db = CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))
    
    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return names[index]
def main(image,seg):
	try:
		segmask,output = seg.segmentImage(image, show_bboxes=False, extract_segmented_objects= True, save_extracted_objects=True)
		#segment = segmask['extracted_objects']
		classes = segmask['class_ids']
		mas = []
		for ip in sorted(glob.glob(os.path.join("*.jpg"))):
			mas.append(ip)
		d = {0: u'background', 1: u'person', 2: u'bicycle', 3: u'car', 4: u'motorcycle', 5: u'airplane', 6: u'bus', 7: u'train', 8: u'truck', 9: u'boat', 10: u'traffic light', 11: u'fire hydrant', 12: u'stop sign', 13: u'parking meter', 14: u'bench', 15: u'bird', 16: u'cat', 17: u'dog', 18: u'horse', 19: u'sheep', 20: u'cow', 21: u'elephant', 22: u'bear', 23: u'zebra', 24: u'giraffe', 25: u'backpack', 26: u'umbrella', 27: u'handbag', 28: u'tie', 29: u'suitcase', 30: u'frisbee', 31: u'skis', 32: u'snowboard', 33: u'sports ball', 34: u'kite', 35: u'baseball bat', 36: u'baseball glove', 37: u'skateboard', 38: u'surfboard', 39: u'tennis racket', 40: u'bottle', 41: u'wine glass', 42: u'cup', 43: u'fork', 44: u'knife', 45: u'spoon', 46: u'bowl', 47: u'banana', 48: u'apple', 49: u'sandwich', 50: u'orange', 51: u'broccoli', 52: u'carrot', 53: u'hot dog', 54: u'pizza', 55: u'donut', 56: u'cake', 57: u'chair', 58: u'couch', 59: u'potted plant', 60: u'bed', 61: u'dining table', 62: u'toilet', 63: u'tv', 64: u'laptop', 65: u'mouse', 66: u'remote', 67: u'keyboard', 68: u'cell phone', 69: u'microwave', 70: u'oven', 71: u'toaster', 72: u'sink', 73: u'refrigerator', 74: u'book', 75: u'clock', 76: u'vase', 77: u'scissors', 78: u'teddy bear', 79: u'hair drier', 80: u'toothbrush'}
		l1 = []
		l2 = []
		l3 = []
		l4 = []
		for cl, ma in zip(classes, mas):
			a = d[cl]
			print(a)
			f = open(ma, 'rb')
			print('start')
			contents = f.read()
			en = base64.b64encode(contents)
			print('done')
			f.close()
			cf = ColorThief(ma)
			dc = cf.get_color(quality=1)
			color_name = convert_rgb_to_names((dc))
			print(color_name)
			l4.append(image.split('.')[0].split('/')[1])
			l1.append(a)
			l2.append(color_name)
			l3.append(en)
			os.remove(ma)		
		df = pd.DataFrame()
		df['segment'] = l4
		df['item'] = l1
		df['color'] = l2
		df['img'] = l3
		print(df)
		Exist = os.path.exists('master.csv')
		if Exist is False:
			df.to_csv('master.csv',index=False,mode='a')
		else:
			df.to_csv('master.csv',index=False,header=False,mode='a')
	except Exception as e:
		return e

if __name__ == "__main__":
	seg = instance_segmentation()
	seg.load_model("mask_rcnn_coco.h5")
	for img_path in sorted(glob.glob(os.path.join('images', "*.jpg"))):
		a = main(img_path,seg)
		print(a)

