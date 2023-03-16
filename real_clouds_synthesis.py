import cv2
import os
import pandas as pd
import shutil
import numpy as np


def cut_img_by_xy(src_dir_path, x_min, x_max, y_min, y_max, save_dir_path):
    name_lst = os.listdir(src_dir_path)
    for name in name_lst:
        img_path = os.path.join(src_dir_path, name)

        img = cv2.imread(img_path, 0)
        img_crop = img[x_min : x_max, y_min : y_max]
        
        save_path = os.path.join(save_dir_path, name)
        cv2.imwrite(save_path, img_crop)


if __name__ == '__main__':
    # =============================================
    ## COMBINE DIFFERENT SPECTRAL BANDS OF CLOUDS WITH THE CHANNELS OF RGB IMAGES
    # =============================================

    # SELECT SPECIFIC CLOUD IMAGES AND ITS CORRESONDING GROUND-TRUTH MASKS IN 38-CLOUD TRAINING DATASET
    src_dir = 'E:\DataSet\\real-clouds-contamination\cloud_mask\\blue'
    src_img_name_lst = os.listdir(src_dir)

    tgt_band_lst = ['green', 'red', 'gt']
    tgt_dir = 'E:\DataSet\\38-Cloud Dataset\\38-Cloud_training'
    for src_img_name in src_img_name_lst:
        for tgt_band in tgt_band_lst:
            tgt_img_path = os.path.join(tgt_dir, 'train_' + tgt_band, src_img_name.replace('blue', tgt_band))
            shutil.copy(tgt_img_path, src_dir.replace('blue', tgt_band))
    print('Finish Moving')

    # RESIZE CLOUD MASKS INTO 256*256
    src_dir_path = 'E:\DataSet\\real-clouds-contamination\cloud_mask'
    save_dir_path = 'E:\DataSet\\real-clouds-contamination\cloud_mask_resized'
    band_name_lst = ['blue', 'green', 'red', 'gt']
    x_min = y_min = 192 - 128
    x_max = y_max = 192 + 128
    for band_name in band_name_lst:
        cut_img_by_xy(os.path.join(src_dir_path, band_name), x_min, x_max, y_min, y_max, os.path.join(save_dir_path, band_name))

    # NORMALIZE EACH BAND OF CLOUD MASKS SEPERATELY
    src_dir = 'E:\DataSet\\real-clouds-contamination\cloud_mask_resized'
    tgt_dir = 'E:\DataSet\\real-clouds-contamination\cloud_mask_resized_normed'
    band_name_lst = ['blue', 'green', 'red']
    img_name_lst = os.listdir(os.path.join(src_dir, 'red'))

    MIN, MAX = 0, 255
    for img_name in img_name_lst:
        for band_name in band_name_lst:
            img = cv2.imread(os.path.join(src_dir, band_name, img_name.replace('red', band_name)), 0)
            
            max_v, min_v = img.max(), img.min()
            fac = (MAX - MIN) / (max_v - min_v)
            img_normed = MIN + fac * (img - min_v)

            cv2.imwrite(os.path.join(tgt_dir, band_name, img_name.replace('red', band_name)), img_normed.astype(np.uint8))

    # COMBINE SPECTRAL BANDS OF CLOUDS WITH THE RGB IMAGES
    band_corr = {'hrb2': 'blue', 'hrb3': 'green', 'hrb4': 'red'}
    cloud_dir = 'E:\DataSet\\real-clouds-contamination\cloud_mask_resized_normed'
    opt_dir = 'E:\DataSet\\real-clouds-contamination'
    opt_name_lst = os.listdir(os.path.join(opt_dir, 'hrb4')) # NAMES OF IMAGE IN DIFFERENT BANDS ARE THE SAME
    cloud_name_lst = os.listdir(os.path.join(cloud_dir, 'red'))
    
    # READ THE RELATIONSHIPS OF IMAGE NAMES BETWEEN BEFORE AND AFTER SHUFFLING    
    tgt2mask_name_corr = {}
    num_mask = len(cloud_name_lst)
    for idx in range(len(opt_name_lst)):  # WHICH IMAGE
        cloudy_img_lst = []
        tgt2mask_name_corr[opt_name_lst[idx]] = cloud_name_lst[idx % num_mask].replace('red', 'gt')    # RECORD WHICH MASK IS USED FOR SYNTHESIZING A GIVEN CLOUDY IMAGE
        for opt_band_name, cloud_band_name in band_corr.items():  # WHICH BAND
            cloud_img = cv2.imread(os.path.join(cloud_dir, cloud_band_name, cloud_name_lst[idx % num_mask].replace('red', cloud_band_name)), 0)
            opt_img = cv2.imread(os.path.join(opt_dir, opt_band_name, opt_name_lst[idx]), 0)
            bin_gt_img = cv2.imread(os.path.join(cloud_dir, 'gt', cloud_name_lst[idx % num_mask].replace('red', 'gt')), 0)

            alpha = cloud_img / 255.  # GET A ALPHA MAP FOR ALPHA BLENDING PROCESS
            alpha = np.clip(alpha * 1.5, 0, 1)  # MAKE THE WEIGHTS OF THIN CLOUDS REGION LARGER FOR A CONTINUOUS BORDER OF CLOUDS
            cloudy_img_lst.append(((1 - alpha) * opt_img + alpha * cloud_img).astype(np.uint8))
        
        cloudy_img = np.array(cloudy_img_lst).transpose(1,2,0)
        cv2.imwrite(os.path.join(opt_dir, 'cloudy rgb', opt_name_lst[idx]), cloudy_img)

        shutil.copy(os.path.join(cloud_dir, 'gt', tgt2mask_name_corr[opt_name_lst[idx]]), os.path.join(opt_dir, 'gt', opt_name_lst[idx]))