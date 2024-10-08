from cam_io import EOS
import os
import datetime
import pathlib
import yaml

'''
This is a useful script for manually recording some images for calibration purposes.
It sets the camera to burst mode and records a quick series of images. 
During the burst, autofocus is disabled and can not adjust, so make sure to position calibration pattern only within the bound of the depth of field.
Move the calibration pattern around in the camera's field of view to get a good spread of images. All images are saved in the target directory.
Make sure the environment is well lit so the shutter speed is fast enough to avoid motion blur.
'''

duration = 100 # duration of the burst in seconds
target_dir = '/home/kh790/data/calibration_imgs/intrinsics'
lens_id = 0

# create a new sub-directory at the target location so that images from each run are kept separate
stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
im_dir = os.path.join(target_dir, stamp)
os.mkdir(im_dir)

calibr_dir = str(pathlib.Path(__file__).parent.parent.resolve()) + '/config' # default location is the config directory of this package
with open(calibr_dir + '/lens_config.yaml', 'r') as f:
    lens_data = yaml.safe_load(f)
focus_dist = lens_data[lens_id]['set_focus_distance']
aperture = lens_data[lens_id]['min_aperture']

# Initialise camera
cam1 = EOS()# if you don't specify a port, the first camera found will be used
capture_params=[aperture,'AUTO','AUTO',False] # small aperture, fast shutter, to avoid Bokeh effects and motion blur
cam1.set_capture_parameters(*capture_params)

cam1.fixed_focus(focus_dist) # set focus distance to the specified value

success, files, msg = cam1.capture_burst(t=duration) # capture a burst of images, t is duration in seconds
for path in files:
    # Now files need to be downloaded from the camera storage to the PC, which might take a while
    # Files are named in ascending alpha-numeric order, so they can be sorted by name
    cam1.download_file(path, target_file=os.path.join(im_dir,path.split('/')[-1]))

print("Data recording done. Images saved in: ", im_dir)