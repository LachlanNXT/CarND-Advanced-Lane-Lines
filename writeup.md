## Writeup

**Advanced Lane Finding Project**

NOTE: code and some of this writeup updated to reflect review comments.

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./output_images/corners.jpg "Corners"
[image2]: ./output_images/undist.jpg "Undistorted"
[image3]: ./test_images/straight_lines1.jpg "Distorted"
[image4]: ./output_images/undist_straight_lines1.jpg "Undistorted"
[image5]: ./output_images/pipeline.png "Pipeline"
[image6]: ./output_images/test4.jpg_final.jpg "Output"
[video1]: ./project_video.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

All code for this project is contained within the lane_finding.ipynb ipython notebook in this repository.

### Camera Calibration

Camera Calibration is the first step for this project. This is done exactly as explained in the example writeup. There are 9 intersection points along the x axis and 6 intersection points along the y axis for the "chessboard" in the calibration pictures. These are used as reference points to transform between real-world coordinates and image coordinates. "Object points", 3d points in real world space are prepared assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image. "Image Points", 2d points in image plane, are detected using cv2 functions. The object points are unique to the chessboard but the same in all images of it, thus `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 

![alt text][image1] ![alt text][image2]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

Distortion correction is applied to each input image in the pipeline using the coeffiecients found during the Camera Calibration step, and `cv2.undistort()`. An example of a distortion corrected road image is below.
Original:
![alt text][image3]
Corrected:
![alt text][image4]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

NOTE: Functions for this are implemented, but not used. Based on reviewer advice, I changed my binary image to use a HSV yellow selector and an RGB white selector as found in "Alternative binary image functions" in the notebook.

I used a combination of:
* Applying Sobel thresholding in x
* Magnitude of the gradient
* Direction of the gradient
* HLS selection

to generate a binary image.

Direction of gradient and Magnitude were noisy measurements, so I used logical and between them and logical or between the result of this, HLS selection, and Sobel in x. With some tuning this produced reasonable results on the test images, i.e. below. This image also shows subsequent pipeline steps discussed below.

![alt text][image5]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The perspective transform cell in the ipython notebook contains a function corners_unwarp(img, M = M), which is used in the main pipeline on the masked combined binary. It is applied after the binary operations so that the edges of the transform are not picked up in any of the binary operations (same applies to the masking operation). This function takes an image and a transformation matrix (pre-computed to save time in the pipeline) and outputs the transformed image.

The source (`src`) and destination (`dst`) points used to calculate the transformation matrix were chosen based on an example image of a straight section of road. The only stipulation to the manual selection process is that the transform is symetrical about the y axis of the image. This makes sure that a centred car looks centred after transformation.

This resulted in the following source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 570, 446      | 40, 0        | 
| 710, 446      | 1240, 0      |
| 90, 650     | 80, 700      |
| 1190, 650      | 1200, 700        |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

In the pipeline section of the code I used the "Peaks in a Histogram" plus sliding window technique found in the course materials to identify lane lines and fit polynomials. A minor change which impproved performance was checking the distance between lines, and if it was too different to the expected value, forcing the lane location of the side with higher variance to be the correct distance from the side with the least variance.

See pipeline image above (Lines?)

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

This is also implemented in the pipeline section and is exactly as explained in the course materials, just adjusted and put into the right order in the pipline. I calculate the radius of curvature from the pixels to metres conversion constant provided and the quadratic fit to the lane line. I was able to do this because my perspective transform was very similar to the example.

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

Once lane lines were found I made a binary image of a solid lane detection and performed the inverse perspective transform, then overlayed this onto the original image (all within the pipeline section of the code). I also overlayed a text display of the radius of curvature. For example, see here:

![alt text][image6]

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video_out.mp4)
The pipeline implemented here does a reasonable job on the basic project video with minor wobbles but no catastrophic failures.

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

The major failings of this implementation are that due to time contraints I basically implemented the most basic and straightforward version of the algorithms that worked, and included none of the more advanced methods that would improve performance. This is evident in the fact that it works ok on the project video, but even on the first challenge video it fails quite badly.

Given more time, I think the most valuable feature to add would be a history of lane characteristics (location, curvature etc.) so that the lanes aren't found from scratch each time and the abberations are smoothed out.
