import tkinter as tk
from tkinter import ttk
from tkinter import Button
from calibrate_camera_tab import CalibrateCameraTab
from train_tab import TrainTab
from preprocess_tab import PreprocessTab
from pypylon import pylon
from basler_cam import BaslerCam


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # create the basler camera instances
        self.top_left_cam = BaslerCam(pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice()), "Top Left Camera")
        self.top_right_cam = BaslerCam(pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice()), "Top Right Camera")
        self.side_cam = BaslerCam(pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice()), "Side Camera")
        self.cameras = [self.top_left_cam, self.top_right_cam, self.side_cam]

        self.main_tab_control = ttk.Notebook(self)
        self.train_tab = TrainTab(self, self.cameras)                                   # create a tab view for the train tab
        self.calibrate_camera_tab = CalibrateCameraTab(self, self.cameras)              # create a tab view for the calibrate tab
        self.preprocess_tab = PreprocessTab(self, self.cameras)                         # create a tab view for the pre-process tab

        self.main_tab_control.add(self.train_tab, text="Train")                         # add the tab for threshold image view
        self.main_tab_control.add(self.calibrate_camera_tab, text="Calibrate Camera")   # add the tab for normal image view
        self.main_tab_control.add(self.preprocess_tab, text="Preprocess")               # add the tab for threshold image view
        
        # pack the tab control
        self.main_tab_control.pack(side="top", fill="both", expand=True)

        # create a button for starting the inspection
        self.start_inspection_button = tk.Button(self, text="Start Inspection")
        self.start_inspection_button.pack(side="right")

        # create a button to set the part delay time (in ms)
        tk.Label(self, text="Part Delay Time (ms)").pack(side="left")
        self.part_delay_time = tk.Entry(self)
        self.part_delay_time.pack(side="left")
        

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1366x728")
    root.resizable(0, 0)
    root.title("Vision Inspection System")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()