# MDF-CR
Official Pytorch code for "SAR and Optical Image Fusion for Cloud Removal via Disentangled Representation"
(As soon as the paper is accepted, I will share my code.)

## License
All rights reserved. The code is released for academic research use only.

## Dataset
In our experiments, I use two different datasets, which I refer to as the [TGRS-SQ](https://datahub.io/lwb19910620/dataset_tgrs-2018-01535-dull-seahorse-98) dataset and the [SEN1-2](https://mediatum.ub.tum.de/1436631) dataset, respectively. More information will be provided below.

- **TGRS-SQ Dataset**
  First, I create a dataset of 1200 images by combining the images from paths "Dataset_TGRS-2018-01535\train\rgb" and "Dataset_TGRS-2018-01535\test_simu\rgb". From this dataset, 1000, 100, and 100 arbitrarily selected images are then used as the training set, validation set, and testing set, respectively. We apply the same processing to the SAR images in "Dataset_TGRS-2018-01535\train\sar" and "Dataset_TGRS-2018-01535\test_simu\sar". It is worth noting that each pair of SAR and RGB images has the same name.
  (Note: This dataset appears to be unavailable, so please try requesting it from the provider if necessary.)
- **SEN1-2-0.85k Dataset**
  Using RGB images as an example, I first select a subset "ROIs1158_spring_s2_2" of 990 images from the SEN1-2 dataset, from which 850, 70, and 70 images are chosen at random as the training set, validation set, and testing set, respectively. For SAR images, I simply select the subset "ROIs1158_spring_s1_2" and perform the same operations as described above.

- **SEN1-2-0.9k Dataset**
  Using RGB images as an example, I first select a subset "ROIs1158_spring_s2_111" of 1106 images from the SEN1-2 dataset, from which 900, 103, and 103 images are chosen at random as the training set, validation set, and testing set, respectively. For SAR images, I simply select the subset "ROIs1158_spring_s1_111" and perform the same operations as described above.
  
The filenames in the three subsets listed above are saved in "**FileNameList.txt**" that are organized similarly. To demonstrate, I use the SEN1-2-0.85k dataset as an example.

```
|——Dataset Name:
|   |——train:
|   |   |——sar:
|   |   |   |——ROIs1158_spring_s1_2_p1.png
|   |   |   |——...
|   |   |——rgb:
|   |   |   |——ROIs1158_spring_s2_2_p1.png
|   |   |   |——...
|   |——val:
|   |   |——sar:
|   |   |   |——ROIs1158_spring_s1_2_p9.png
|   |   |   |——...
|   |   |——rgb:
|   |   |   |——ROIs1158_spring_s2_2_p9.png
|   |   |   |——...
|   |——test:
|   |   |——sar:
|   |   |   |——ROIs1158_spring_s1_2_p25.png
|   |   |   |——...
|   |   |——rgb:
|   |   |   |——ROIs1158_spring_s2_2_p25.png
|   |   |   |——...
```

## Real Clouds Synthesis
We choose nine real cloudy images at random from the 38-Cloud dataset. The clouds in them are then combined with cloudless RGB images from the TGRS-SQ test dataset to create 100 cloudy images. The filenames of nine selected real cloudy images, as well as their connections with the cloudless RGB images during synthesis, are shown in " **src2mask_name_corr.csv**".

In addition, I'll explain how to synthesize real cloudy images in "**real_clouds_synthesis.py**" for your convenience. The associated files must be organized as follows:
```
|——real-clouds-contamination:
## destination files
|   |——gt
|   |——cloudy rgb
|   |——rgb
|   |——sar

## temporary files
|   |——hrb4
|   |——hrb3
|   |——hrb2
|   |   |——cloud_mask
|   |   |   |——blue
|   |   |   |——green
|   |   |   |——red
|   |   |   |——gt
|   |   |——cloud_mask_resized
|   |   |   |——blue
|   |   |   |——green
|   |   |   |——red
|   |   |   |——gt
|   |   |——cloud_mask_resized_normed
|   |   |   |——blue
|   |   |   |——green
|   |   |   |——red
|   |   |   |——gt
```
where you should select some real cloudy images from the 38-Cloud dataset and place them in ```E:\DataSet\\real-clouds-contamination\cloud_mask\\blue```. At the same time, you must relocate the images in the test set's five channels (```sar```,```rgb```, ```hrb4```, ```hrb3``` and ```hrb2```) from the predecessor of the TGRS-SQ dataset to the positions indicated above. We are now prepared to begin the synthesis procedure. Following that, you can obtain our destination folders ```gt```, ```cloudy rgb```, ```rgb``` and ```sar```, and the remaining temporary files can be deleted.

## Contact
If you have any questions or suggestions, feel free to contact me by email: 714848657@qq.com (recommended) or lizijue@mail.nwpu.edu.cn.