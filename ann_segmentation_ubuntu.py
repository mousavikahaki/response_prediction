#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ---------------------------------------------------------------------------
# Created on Fri Nov 12 15:57:37 2021
#
# @author: SeyedM.MousaviKahaki (mousavikahaki@gmail.com)
#----------------------------------------------------------------------------
# Title:        Annotation Segmentation (Ubuntu)
#
# Description:  This code perform segmentation on annotations to separate tissue and the background
#               
#
#
# Input:        String: Source directory with extracted annotations   
# Output:       Segmented annotations
#
# 
# Example:      ann_segmentation_ubuntu.py
#
#
# version ='3.0'
# ---------------------------------------------------------------------------
"""
Created on Fri Nov 12 15:57:37 2021

@author: SeyedM.MousaviKahaki
"""


from PIL import Image, ImageDraw#, ImageOps
import cv2
import matplotlib.pyplot as plt
import numpy as np
# from skimage import data
from skimage.filters import threshold_otsu
import os
import glob
from pathlib import Path




INPUTDIR = '/home/seyedm.mousavikahaki/Documents/wxc4/Data/'
OUTPUTDIR = '/home/seyedm.mousavikahaki/Documents/wxc4/Segmented/'

root_directory = glob.glob(r''+INPUTDIR+'*')

##############################
#get current dir
cwd = os.getcwd()

jpg_file=".jpg"
png_file=".png"


png_dir = Path(OUTPUTDIR)
png_dir.mkdir(parents=True, exist_ok=True)

png_dir=OUTPUTDIR


#for on all folders
for filename in root_directory:
   
    groupname = filename.split("\\")[-1]
   
    chck_group_name=True
        
   
   
    files = glob.glob( filename + r"/*.jpg")

    files_clean = []
    # exclude mask images
    # i=0
    for r in files:
        #print(r)
        a= r.split("\\")[-1]
        b= a.split(".")[0]
        c=b.find("mask")
        # if(c>-1):
        #     rt=files.pop()[i]\
        if(c==-1):
            files_clean.append(r)
        # i=i+1
 
  
    # for on  all images in a folder
    for fl in files_clean:
      
        a= fl.split("/")[-1]
        fileName= a.split(".")[0]
        

        
        img = cv2.imread(fl, cv2.IMREAD_COLOR)
        # img = Image.open(fl)
        #read grayscale
        image = cv2.imread(fl, cv2.IMREAD_GRAYSCALE)
        
        #OTSU Thresholding
        thresh = threshold_otsu(image)
        seed = (0, 0)
        rep_value = (0, 0, 0, 0)
        print("Processing " + fl)
        
        # Add Border to image
        h,w=image.shape[0:2]
        base_size=h+40,w+40,3
        # make a 3 channel image for base which is slightly larger than target img
        base=np.zeros(base_size,dtype=np.uint8)
        cv2.rectangle(base,(0,0),(w+20,h+20),(255,255,255),30) # really thick white rectangle
        base[10:h+10,10:w+10]=img # this works
        img1=Image.fromarray(base)
        
        
        ImageDraw.floodfill(img1, seed, rep_value, thresh = thresh)#220)
        
        img1.save("C:/DATA/tmp/"+fileName+png_file)
        
        file_name = "C:/DATA/tmp/"+fileName+png_file
        
        src = cv2.imread(file_name, 1)
        tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        _,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
        b, g, r = cv2.split(src)
        rgba = [b,g,r, alpha]
        dst = cv2.merge(rgba,4)
        pixels = np.where(dst[:][:] ==[0,0,0,0], [255,255,255,255], dst)
         
        png_dir = Path(OUTPUTDIR+groupname)
        png_dir.mkdir(parents=True, exist_ok=True)
        
        cv2.imwrite(OUTPUTDIR+groupname+"/"+fileName+"_Segmented"+jpg_file , pixels)
        print("File Saved:  " + OUTPUTDIR+groupname+"/"+fileName+"_Segmented"+jpg_file)


