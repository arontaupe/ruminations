import pandas as pd
import cv2
import time
from datetime import datetime
import numpy as np
import pyaudio

show_debug = False
contoursize = 12000 # motion sensitivity. higher is less sensitive. default: 10000
sensitivity = 50 # binary threshold. higher is less sensitive. default: 30
deepfactor = 15

# Assigning our initial state in the form of variable initialState as None for initial frames
initialState = None
# List of all the tracks when there is any detected of motion in the frames
motionTrackList = [None, None]
# A new list 'time' for storing the time when movement detected
motionTime = []
# Initialising DataFrame variable 'dataFrame' using pandas libraries panda with Initial and Final column
df = pd.DataFrame(columns=["Initial", "Final"])
# starting the webCam to capture the video using cv2 module
video = cv2.VideoCapture(0)
start_time = time.time()
ref_time = time.time()

interval = 3.0
blursize = 21

def get_average(img):
	average_color_row = np.average(img, axis=0)
	average_color = np.average(average_color_row, axis=0)
	return average_color

def play_sound(brightness, deepfactor):
	p = pyaudio.PyAudio()
	volume = 0.5  # range [0.0, 1.0]
	fs = 44100  # sampling rate, Hz, must be integer
	duration = 0.2  # in seconds, may be float
	f = brightness / deepfactor # sine frequency, Hz, may be float

	# generate samples, note conversion to float32 array
	samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)
	# per @yahweh comment explicitly convert to bytes sequence
	output_bytes = (volume * samples).tobytes()

	# for paFloat32 sample values must be in range [-1.0, 1.0]
	stream = p.open(format=pyaudio.paFloat32,
	                channels=1,
	                rate=fs,
	                output=True
	                )
	# play. May repeat with different volume values (if done interactively)
	start_time = time.time()
	stream.write(output_bytes)
	if(show_debug):
		print("Played sound for {:.2f} seconds".format(time.time() - start_time))
	stream.stop_stream()
	stream.close()
	p.terminate()


# using infinite loop to capture the frames from the video
while True:
	# Reading each image or frame from the video using read function
	check, cur_frame = video.read()
	# Defining 'motion' variable equal to zero as initial frame
	var_motion = 0
	# From colour images creating a gray frame
	gray_image = cv2.cvtColor(cur_frame, cv2.COLOR_BGR2GRAY)
	# To find the changes creating a GaussianBlur from the gray scale image
	gray_frame = cv2.GaussianBlur(gray_image, (blursize, blursize), 0)
	# For the first iteration checking the condition
	# we will assign grayFrame to initalState if is none
	if time.time() - ref_time > interval:
		initialState = None
		ref_time = time.time()
		if (show_debug):
			print("Img Reset")

	if initialState is None:
		initialState = gray_frame
		continue

	# Calculation of difference between static or initial and gray frame we created
	differ_frame = cv2.absdiff(initialState, gray_frame)
	# the change between static or initial background and current gray frame are highlighted
	thresh_frame = cv2.threshold(differ_frame, sensitivity, 255, cv2.THRESH_BINARY)[1]
	thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)
	# For the moving object in the frame finding the coutours
	cont, _ = cv2.findContours(thresh_frame.copy(),
	                           cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
	                           )
	for cur in cont:
		if cv2.contourArea(cur) < contoursize:
			continue
		var_motion = 1

		play_sound(cv2.contourArea(cur), deepfactor)

		(cur_x, cur_y, cur_w, cur_h) = cv2.boundingRect(cur)
		# To create a rectangle of green color around the moving object
		cv2.rectangle(differ_frame, (cur_x, cur_y), (cur_x + cur_w, cur_y + cur_h), (255), 1)

	# from the frame adding the motion status
	motionTrackList.append(var_motion)
	motionTrackList = motionTrackList[-2:]
	# Adding the Start time of the motion
	if motionTrackList[-1] == 1 and motionTrackList[-2] == 0:
		motionTime.append(datetime.now())
	# Adding the End time of the motion
	if motionTrackList[-1] == 0 and motionTrackList[-2] == 1:
		motionTime.append(datetime.now())
	# In the gray scale displaying the captured image
	# cv2.imshow("The image captured in the Gray Frame is shown below: ", gray_frame)
	# To display the difference between inital static frame and the current frame
	cv2.imshow("Difference between the  inital static frame and the current frame: ", differ_frame)
	# To display on the frame screen the black and white images from the video
	# cv2.imshow("Threshold Frame created from the PC or Laptop Webcam is: ", thresh_frame)
	# Through the colour frame displaying the contour of the object
	# cv2.imshow("From the PC or Laptop webcam, this is one example of the Colour Frame:", cur_frame)
	# Creating a key to wait
	wait_key = cv2.waitKey(1)
	# With the help of the 'm' key ending the whole process of our system
	if wait_key == ord('m'):
		# adding the motion variable value to motiontime list when something is moving on the screen
		if var_motion == 1:
			motionTime.append(datetime.now())
		break

# At last we are adding the time of motion or var_motion inside the data frame
for a in range(0, len(motionTime), 2):
	row = pd.DataFrame({"Initial": motionTime[a], "Final": motionTime[a + 1]}, index=[0])
	df = pd.concat([df, row], ignore_index= True)
# To record all the movements, creating a CSV file
df.to_csv("EachMovement.csv")

# Releasing the video
video.release()
# Now, Closing or destroying all the open windows with the help of openCV
cv2.destroyAllWindows()
