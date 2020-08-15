from cv2 import cv2
import tkinter as tk
from tkinter import ttk
from custom_widgets import CameraViewWidget
from utils import update_tk_frame

class TrainTab(ttk.Frame):
    def __init__(self, parent, cameras, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.cameras = cameras
        self.selected_cam = cameras[0]

        self.cam_view_widget = CameraViewWidget(self, self.cameras, self.cam_view_on_click)
        self.cam_view_widget.pack(side="left")

        self.cam_frame = tk.Label(self, text="Select a camera instance")
        self.cam_frame.pack()

        self.start_train_button = tk.Button(self, text="Start Training")
        self.start_train_button.pack()

        self.update_cam_frame()
    
    def cam_view_on_click(self, event):
        w = event.widget
        self.cam_frame.configure(text=w.cget("text"), compound=tk.BOTTOM)
        self.selected_cam = next(cam for cam in self.cameras if cam.camera_name == w.cget("text"))
        self.update_cam_frame()

    def update_cam_frame(self):
        if self.selected_cam != None:
            img = self.selected_cam.grab_single_image()
            update_tk_frame(self.cam_frame, img, size=(600, 300))
            self.cam_view_widget.refresh_cam(self.cameras.index(self.selected_cam), img)