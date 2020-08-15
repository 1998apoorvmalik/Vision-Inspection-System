import tkinter as tk
from tkinter import ttk
from custom_widgets import CameraViewWidget
from utils import update_tk_frame
import time

class CalibrateCameraTab(ttk.Frame):
    def __init__(self, parent, cameras, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.cameras = cameras
        self.selected_cam = cameras[0]

        self.cam_view_widget = CameraViewWidget(self, self.cameras, self.cam_view_on_click)
        self.cam_view_widget.pack(side="left")

        self.cam_frame = tk.Label(self, text="Select a camera instance")
        self.cam_frame.pack()

        self.auto_exposure_val = tk.IntVar()
        tk.Checkbutton(self, text="Auto Exposure", var=self.auto_exposure_val, command=self.refresh).pack()

        self.auto_gain_val = tk.IntVar()
        tk.Checkbutton(self, text="Auto Gain", var=self.auto_gain_val, command=self.refresh).pack()

        self.white_balance_val = tk.IntVar()
        tk.Checkbutton(self, text="Auto Whitebalance", var=self.white_balance_val, command=self.refresh).pack()

        self.gain_slider = tk.Scale(self, orient=tk.HORIZONTAL, label="Gain", from_=0, to=240, length=300, command=self.gain_slider_on_change)
        self.gain_slider.pack()

        """ Setting up exposure adjustiment widget """
        self.exposure_frame = tk.Frame(self)
        tk.Label(self.exposure_frame, text="Exposure time (ms)").grid(row=1, column=0, pady=5)
        self.exposure_entry_var = tk.IntVar()
        self.exposure_entry_field = tk.Entry(self.exposure_frame, textvariable=self.exposure_entry_var)
        self.exposure_entry_field.bind("<Key-Return>", self.exposure_entry_on_change)
        self.exposure_entry_field.grid(row=1, column=1)
        tk.Label(self.exposure_frame, text="(Min: 1000, Max: 100000)").grid(row=1, column=2)
        self.exposure_frame.pack()
        self.exposure_slider = tk.Scale(self, orient=tk.HORIZONTAL, from_=1000, to=100000, length=300, command=self.exposure_slider_on_change)
        self.exposure_slider.pack()
        
        self.refresh()
        
    def refresh(self):
        if self.white_balance_val.get() == 1:
            self.selected_cam.whiteBalance = "Continuous"
        else:
            self.selected_cam.whiteBalance = "Off"

        if self.auto_exposure_val.get() == 1:
            self.exposure_slider.configure(state="disabled")
            self.exposure_entry_field.configure(state="disabled")
            self.selected_cam.autoExposure = "Continuous"
        else:
            self.exposure_slider.configure(state="normal")
            self.exposure_entry_field.configure(state="normal")
            self.selected_cam.autoExposure = "Off"

        if self.auto_gain_val.get() == 1:
            self.gain_slider.configure(state="disabled")
            self.selected_cam.autoGain = "Once"
        else:
            self.gain_slider.configure(state="normal")
            self.selected_cam.autoGain = "Off"

        self.exposure_entry_var.set(self.selected_cam.exposureTime)
        self.gain_slider.set(self.selected_cam.gain)
        self.exposure_slider.set(self.selected_cam.exposureTime)
        self.update_cam_frame()
    
    def cam_view_on_click(self, event):
        w = event.widget
        self.cam_frame.configure(text=w.cget("text"), compound=tk.BOTTOM)
        self.selected_cam = next(cam for cam in self.cameras if cam.camera_name == w.cget("text"))
        self.update_cam_frame()
    
    def exposure_slider_on_change(self, val):
        self.selected_cam.exposureTime = float(val)
        self.refresh()
    
    def exposure_entry_on_change(self, event):
        exposureTime = self.exposure_entry_var.get()
        if exposureTime >= 1000 and exposureTime <= 100000:
            self.selected_cam.exposureTime = exposureTime
        self.refresh()
    
    def gain_slider_on_change(self, val):
        self.selected_cam.gain = int(val)
        self.refresh()
    
    def update_cam_frame(self):
        if self.selected_cam != None:
            img = self.selected_cam.grab_single_image()
            update_tk_frame(self.cam_frame, img, size=(600, 300))
            self.cam_view_widget.refresh_cam(self.cameras.index(self.selected_cam), img)
