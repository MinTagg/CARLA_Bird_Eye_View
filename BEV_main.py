#!/usr/bin/env python

import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import random
import time

import numpy as np
import cv2
import rospy
import cv_bridge
from sensor_msgs.msg import Image
import util.BEV as bev
import argparse
import datetime

actor_list = []
IM_WIDTH = 1024
IM_HEIGHT = 1024

def publish_img(image,pub):
    i = np.ndarray(shape=((image.height, image.width, 4)), dtype=np.uint8, buffer=image.raw_data)[:, :, 0:3]
    i = bev.main(i)
    pub.publish(cv_bridge.CvBridge().cv2_to_imgmsg(np.array(i), encoding='passthrough'))
    
def save_img(image, directory, suffix):
    i = np.ndarray(shape=((image.height, image.width, 4)), dtype=np.uint8, buffer=image.raw_data)[:, :, 0:3]
    i = bev.main(i)
    ### 저장 코드 넣기
    if not os.path.isdir(directory):
        os.mkdir(directory)
    path = f'{directory}/{str(suffix)}.jpg'
    cv2.imwrite(path, i)

suffix = 0

parser = argparse.ArgumentParser()

parser.add_argument('--save', default=True, help = 'Save BEV image (default = True)')
parser.add_argument('--publish', default=False, help='Publish BEV image (default = False, Default Topic = Image/BEV/Front)')
args = parser.parse_args()
start = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(20)

    world = client.get_world()
    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.no_rendering_mode = False
    settings.fixed_delta_seconds = 0.05
    world.apply_settings(settings)

    if args.publish:
        rospy.init_node('Publisher')
        pub = rospy.Publisher('Image/BEV/Front', Image)


    blueprint_library = world.get_blueprint_library()

    bp = blueprint_library.filter('model3')[0]

    spawn_point = random.choice(world.get_map().get_spawn_points())
    vehicle = world.spawn_actor(bp, spawn_point)
    actor_list.append(vehicle)

    # https://carla.readthedocs.io/en/latest/cameras_and_sensors
    # get the blueprint for this sensor
    blueprint = blueprint_library.find('sensor.camera.rgb')
    # change the dimensions of the image
    blueprint.set_attribute('image_size_x', f'{IM_WIDTH}')
    blueprint.set_attribute('image_size_y', f'{IM_HEIGHT}')
    blueprint.set_attribute('fov', '90')
    blueprint.set_attribute('sensor_tick', '0.1')

    cam_location = carla.Location(x=2.5,z=0.7)

    # Adjust sensor relative to vehicle
    spawn_point = carla.Transform(cam_location)

    # spawn the sensor and attach to vehicle.
    sensor = world.spawn_actor(blueprint, spawn_point, attach_to=vehicle)

    # add sensor to list of actors
    actor_list.append(sensor)
    # do something with this sensor

    if args.publish:
        sensor.listen(lambda data: publish_img(data, pub))
    elif args.save:
        sensor.listen(lambda data: save_img(data, start, suffix = suffix))

    while True:
        world.tick()
        if world.tick():
            suffix += 1

        #vehicle.set_autopilot(True)  # if you just wanted some NPCs to drive.

finally:
    settings.synchronous_mode = False
    world.apply_settings(settings)
    print('destroying actors')
    for actor in actor_list:
        actor.destroy()
    print('done.')

