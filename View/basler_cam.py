from pypylon import pylon

imgBSLR_to_imgCV_converter = pylon.ImageFormatConverter()
imgBSLR_to_imgCV_converter.OutputPixelFormat = pylon.PixelType_BGR8packed                   # converting to opencv bgr format
imgBSLR_to_imgCV_converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

class BaslerCam():
    def __init__(self, camera, camera_name="Unamed Camera", show_config=False):
        # initialize the camera object
        self.camera = camera
        self.camera_name = camera_name
       
        # camera configuration settings variables
        self.whiteBalance = None
        self.autoExposure = None
        self.autoGain = None
        self.exposureTime = None
        self.gain = None

        # update camera configuration settings
        self.refresh_camera_config(show_config)

    def refresh_camera_config(self, show_config):
        # start grabbing
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        
        # update the camera configuration settings
        self.whiteBalance = self.camera.BalanceWhiteAuto.GetValue()
        self.autoExposure = self.camera.ExposureAuto.GetValue()
        self.autoGain = self.camera.GainAuto.GetValue()
        self.exposureTime = self.camera.ExposureTimeAbs.GetValue()
        self.gain = self.camera.GainRaw.GetValue()

        # stop grabbing
        self.camera.StopGrabbing()

        if show_config:
            # get camera configuration settings
            self.get_camera_config()
    
    def get_camera_config(self):
        print("\nCamera {} configuration -->".format(self.camera_name))
        print("White Balance : {}".format(self.whiteBalance))
        print("Auto Exposure : {}".format(self.autoExposure))
        print("Auto Gain : {}".format(self.autoGain))
        print("Exposure Time : {}".format(self.exposureTime))
        print("Gain : {}\n".format(self.gain))

        return (self.autoExposure, self.autoGain, self.exposureTime, self.gain)
    
    def grab_single_image(self):
        # start grabbing the images from the camera using the strategy defined below
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImages)

        # set camera config options
        self.get_camera_config()
        if self.autoExposure == "Off":
            self.camera.ExposureTimeAbs.SetValue(self.exposureTime)
        if self.autoGain == "Off":
            self.camera.GainRaw.SetValue(self.gain)

        self.camera.BalanceWhiteAuto.SetValue(self.whiteBalance)
        self.camera.ExposureAuto.SetValue(self.autoExposure)
        self.camera.GainAuto.SetValue(self.autoGain)
        
        while self.camera.IsGrabbing():
            grabResult = self.camera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)
            
            if grabResult.GrabSucceeded():
                # access the image data
                image = imgBSLR_to_imgCV_converter.Convert(grabResult)
                image = image.GetArray()

                # stop grabbing the images from the camera
                self.camera.StopGrabbing()

                # return the cv image
                return image