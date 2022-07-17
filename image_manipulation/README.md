# Image/video manipulation tools

This is a grouping of short scripts that can automate manipulating image and video files. These were born out of individual need, and not wanting to do all of this by hand more than once. 

* frames\_to\_gif.py - Take a sortable group of images and turn them into a gif
	- Depends on natsort library (install this though pip, etc.)
* gif\_to\_frames.py - Take a gif and break it down into individual frames (images)
* vid\_to\_gif.py - Takes a video file (such as a MP4) and directly converts it into a gif.
	- Depends on moviepy library (install this though pip, etc.)