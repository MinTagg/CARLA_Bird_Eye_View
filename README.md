# CARLA_Bird_Eye_View

This file make one single image to Bird's Eye View image

Car :: Tesla Model 3

Output Image Resolution :: (512,665)

If you want to change the input image resolution, you have to calibrate the IMAGE_RATIO in BEV.py

Original Image

![sample](https://user-images.githubusercontent.com/98318559/150778655-77c21191-0c7e-41b3-b38c-2449171045ab.jpg)

Converted Image

![result_image](https://user-images.githubusercontent.com/98318559/150778687-ba0e3c49-2128-434a-b777-a24bef7a4726.jpg)

## Requirments

CARLA : https://carla.readthedocs.io/en/latest/start_quickstart/
ros(Melodic) : http://wiki.ros.org/melodic/Installation/Ubuntu

Checked at Ubuntu 18.04 + ros Melodic

## How to run

```shell
python BEV_main.py
```

Default settings of BEV_main.py is saving BEV image.

At first it will make a directory 'YYYYMMDD_HHMMSS'

BEV image will be saved in the directory.

If you want publish that image through ros

```shell
python BEV_main.py --save False --publish True
```

It will publish the BEV image through ros

Topic name is 'Image/BEV/Front'
