from cv2 import cv2
import tkinter as tk
from tkinter import ttk
from utils import update_tk_frame


class CalibrateImageFrameWidget(tk.Frame):
    def __init__(self, parent, camera_instance, name="Calibrate View", *args, **kwargs,):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.cam = camera_instance                                                      # camera instance

        # lower & upper limits for the threshold image
        self.thresh_lower = 0
        self.thresh_upper = 0

        # lower & upper limits for the canny image
        self.canny_lower = 0
        self.canny_upper = 0

        # create the image frame label
        tk.Label(self, text=name).grid(row=0, column=0, pady=3)

        """ Tab control for multiple pre-processed images """
        self.tab_control = ttk.Notebook(self)                                           # create a tab control
        
        self.raw_image_tab = ttk.Frame(self.tab_control)                                # create a tab for normal image view
        self.threshold_image_tab = ttk.Frame(self.tab_control)                          # create a tab for threshold image view
        self.canny_image_tab = ttk.Frame(self.tab_control)                              # create a tab for canny image view
        
        self.tab_control.add(self.raw_image_tab, text="Raw Image View")                 # add the tab for normal image view
        self.tab_control.add(self.threshold_image_tab, text="Threshold Image View")     # add the tab for threshold image view
        self.tab_control.add(self.canny_image_tab, text="Canny Image View")             # add the tab for canny image view
        # pack the tab control
        self.tab_control.grid(row=1, column=0, pady=5)

        # create the image frame
        self.raw_image_frame = tk.Label(self.raw_image_tab)
        self.threshold_image_frame = tk.Label(self.threshold_image_tab)
        self.canny_image_frame = tk.Label(self.canny_image_tab)
        self.raw_image_frame.pack()
        self.threshold_image_frame.pack()
        self.canny_image_frame.pack()

        # create the refresh-image-frame button
        self.image_frame_refresh_button = tk.Button(self, text="Refresh", command=self.refresh)
        self.image_frame_refresh_button.grid(row=2, column=0)

        self.refresh()
    
    def refresh(self):
        # image updates
        """ Grab the image from the basler camera (already converted to the opencv format) """
        original_image = self.cam.grab_single_image()                                                                   # original Image
        gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)                                                   # gray Image
        blur_image = cv2.GaussianBlur(gray_image, (3, 3), 0)                                                            # blur image                                                             
        _, threshold_image = cv2.threshold(blur_image, self.thresh_lower, self.thresh_upper, cv2.THRESH_BINARY)         # threshold image
        canny_image = cv2.Canny(threshold_image, self.canny_lower, self.canny_upper)                                    # canny image

        # update the image frames
        update_tk_frame(self.raw_image_frame, original_image)
        update_tk_frame(self.threshold_image_frame, threshold_image)
        update_tk_frame(self.canny_image_frame, canny_image)


class ThresholdWidget(tk.Frame):
    def __init__(self, parent, on_change_event, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Frame
        self.threshold_lower_frame = tk.Frame(self)
        self.threshold_upper_frame = tk.Frame(self)
        self.threshold_lower_frame.grid(row=0, column=0, pady=10)
        self.threshold_upper_frame.grid(row=1, column=0)

        # Slider
        self.threshold_lower_slider = tk.Scale(self.threshold_lower_frame, orient=tk.HORIZONTAL, label="Lower Threshold", from_=0, to=255, length=300)
        self.threshold_upper_slider = tk.Scale(self.threshold_upper_frame, orient=tk.HORIZONTAL, label="Upper Threshold", from_=0, to=255, length=300)
        self.threshold_lower_slider.bind("<ButtonRelease-1>", on_change_event)
        self.threshold_upper_slider.bind("<ButtonRelease-1>", on_change_event)
        self.threshold_lower_slider.pack()
        self.threshold_upper_slider.pack()


class CannyEdgeWidget(tk.Frame):
    def __init__(self, parent, on_change_event, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Frame
        self.canny_lower_frame = tk.Frame(self)
        self.canny_upper_frame = tk.Frame(self)
        self.canny_lower_frame.grid(row=0, column=0, pady=10)
        self.canny_upper_frame.grid(row=1, column=0)

        # Slider
        self.canny_lower_slider = tk.Scale(self.canny_lower_frame, orient=tk.HORIZONTAL, label="Lower Canny", from_=0, to=255, length=300)
        self.canny_upper_slider = tk.Scale(self.canny_upper_frame, orient=tk.HORIZONTAL, label="Upper Canny", from_=0, to=255, length=300)
        self.canny_lower_slider.bind("<ButtonRelease-1>", on_change_event)
        self.canny_upper_slider.bind("<ButtonRelease-1>", on_change_event)
        self.canny_lower_slider.pack()
        self.canny_upper_slider.pack()

class CameraViewWidget(tk.Frame):
    def __init__(self, parent, cameras, on_click_event=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.cameras = cameras
        self.camera_frames = []

        for cam in cameras:
            # camera frame name
            cam_frame = tk.Label(self, text=cam.camera_name, compound=tk.CENTER, foreground="white")
            cam_frame.pack()
            self.camera_frames.append(cam_frame)
            
            if on_click_event != None:
                cam_frame.bind("<ButtonRelease-1>", on_click_event)
        
        for cam_index in range(len(self.cameras)):
            self.refresh_cam(cam_index)
            
    def refresh_cam(self, cam_index, image=None):
        cam = self.cameras[cam_index]
        cam_frame = self.camera_frames[cam_index]
        
        if image is not None:
            cam_image = image
        else:
            cam_image = cam.grab_single_image()

        update_tk_frame(cam_frame, cam_image, size=(100, 100))