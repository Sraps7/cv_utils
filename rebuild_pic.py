# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 17:17:41 2020

@author: 28171
"""

import os
import cv2
import numpy as np
import time
import argparse



parser = argparse.ArgumentParser()

parser.add_argument("-f", "--filename", help="path to the img", type=str)
parser.add_argument("--cut_w", help="nums to cut the img along w direction",
                    type=int, default=4)
parser.add_argument("--cut_h", help="nums to cut the img along h direction",
                    type=int, default=4)
parser.add_argument("--line_w", help="split line width", type=int, default=20)
parser.add_argument("--line_auto_w", help="auto choose a split line width",
                    action="store_true")
parser.add_argument("--save", help="if True, save imgs in './combin'", 
                    action="store_true")





def cv_show(img, window="img", adjust=0, resize=False, width=800):
    h, w, c = img.shape
    cv2.namedWindow(window, adjust)
    if resize:
        height = int(h/w*width)
        cv2.resizeWindow(window, width, height)
    
    cv2.imshow(window, img)
    while True:
        char = cv2.waitKey(0)
        if char == ord("q"):
            break
    cv2.destroyWindow(window)

def cut(img, cut_w, cut_h):
    h, w, c = img.shape

    patch_w = w // cut_w
    patch_h = h // cut_h
    
    patches = []
    for i in range(cut_h):
        for j in range(cut_w):
            patches.append(img[i * patch_h : (i+1) * patch_h, j*patch_w:(j+1)*patch_w, :])
    return patches
   
def draw_canvas_random(patches, cut_w, cut_h):
    h, w, c = img.shape
    
    patch_w = w // cut_w
    patch_h = h // cut_h
    
    canvas = np.zeros((patch_h*cut_h, patch_w*cut_w, c), dtype=np.uint8)
    
    idx = list(range(cut_w * cut_h))
    np.random.shuffle(idx)
    
    for i in range(cut_h):
        for j in range(cut_w):
            canvas[i * patch_h : (i+1) * patch_h, j*patch_w:(j+1)*patch_w, :] = patches[idx.pop(0)]
    return canvas

def add_split_line(canvas, cut_w, cut_h, line_w, line_color=0):
    h, w, c = canvas.shape
    patch_w = w // cut_w
    patch_h = h // cut_h
    
    new_h = h + (cut_h-1) * line_w
    new_w = w + (cut_w-1) * line_w
    
    new_canvas = np.zeros((new_h, new_w, c), dtype=np.uint8)
    
    horizontal_line = np.zeros((line_w, new_w, c), dtype=np.uint8)
    vertical_line = np.zeros((new_h, line_w, c), dtype=np.uint8)
    
    if line_color:
        pass
    
    for i in range(cut_w):
        for j in range(cut_h):
            new_canvas[i * (patch_h+line_w) : i * (patch_h+line_w)+patch_h, j * (patch_w+line_w) : j * (patch_w+line_w)+patch_w, :] = canvas[i * patch_h : (i+1) * patch_h, j*patch_w:(j+1)*patch_w, :]
    return new_canvas



if __name__ == "__main__":
    #Hyperparameters
    filename = "portrait-787522_1920.jpg"
    cut_w, cut_h = 4, 4
    line_w = 20
    line_auto_w = True
    save = False
    
    if line_auto_w:
        img = cv2.imread(filename)
        h, w, c = img.shape
        line_w = min(h, w) // 210
    
    patches = cut(img, cut_w, cut_h)
    
    canvas = draw_canvas_random(patches, cut_w, cut_h)
    canvas_with_split_line = add_split_line(canvas, cut_w, cut_h, line_w)
    
    
    cv_show(img, filename, resize=True)
    cv_show(canvas, filename+"-shuffle", resize=True)
    cv_show(canvas_with_split_line, filename+"-shuffle"+"split-line", resize=True)
    
    if save:
        if not os.path.exists("./combine"):
            os.mkdir("./combine")
        basename, extra_name = os.path.basename(filename).split(".")
        cv2.imwrite(os.path.join("./combine", basename + str(int(time.time())) + "." + extra_name), canvas)
        cv2.imwrite(os.path.join("./combine", basename + str(int(time.time())) + "-split-line" + "." + extra_name), canvas_with_split_line)
    
