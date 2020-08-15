import tkinter as tk
from tkinter import ttk
from pypylon import pylon
from custom_widgets import ThresholdWidget
from custom_widgets import CannyEdgeWidget
from custom_widgets import CalibrateImageFrameWidget

class PreprocessTab(ttk.Frame):
    def __init__(self, parent, cameras, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # create a calibrate view for all of the camera instances
        for cam_index in range(len(cameras)):
            calibrate_view = CalibrateView(self, camera_instance=cameras[cam_index], name=cameras[cam_index].camera_name)
            calibrate_view.pack(side="left")

class CalibrateView(tk.Frame):
    def __init__(self, parent, camera_instance, name="Calibrate View", *args, **kwargs,):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # create the calibrate image frame widget
        self.calibrate_image_frame = CalibrateImageFrameWidget(self, camera_instance, name=name)
        self.calibrate_image_frame.grid(row=0, column=0, pady=3)

        # create the select kernel menu
        self.kernel_frame = tk.Frame(self)
        tk.Label(self.kernel_frame, text="Kernal Size").pack(side="left")
        self.kernel_var = tk.StringVar()
        self.kernel_var.set("(3x3)")
        self.kernel_option_list = ["(3x3)", "(5x5)", "(7x7)"]
        self.kernel_menu = tk.OptionMenu(self.kernel_frame, self.kernel_var, *self.kernel_option_list)
        self.kernel_menu.pack(side="left")
        self.kernel_frame.grid(row=1, column=0)

        # create the image threshold widget
        self.image_threshold_widget = ThresholdWidget(self, self.slider_on_change_event)
        self.image_threshold_widget.grid(row=2, column=0)

        # create the canny edge widget
        self.canny_edge_widget = CannyEdgeWidget(self, self.slider_on_change_event)
        self.canny_edge_widget.grid(row=3, column=0)
    
    def slider_on_change_event(self, event):
        w = event.widget
        label = w.cget("label")
        value = w.get()

        if label == "Lower Threshold":
            self.calibrate_image_frame.thresh_lower = value
        elif label == "Upper Threshold":
            self.calibrate_image_frame.thresh_upper = value
        elif label == "Lower Canny":
            self.calibrate_image_frame.canny_lower = value
        else:
            self.calibrate_image_frame.canny_upper = value
        
        self.calibrate_image_frame.refresh()