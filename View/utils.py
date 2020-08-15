from cv2 import cv2
from PIL import Image, ImageTk

def update_tk_frame(frame, image, size=(250,250)):
    # convert the image to tkinter format
    image = imgCV_to_imgTK(image, size)
    # place the image in the defined tkinter frames
    frame.imgtk = image
    # configure the image to display in the respective frame
    frame.configure(image=image)

def imgCV_to_imgTK(image, size):
    # check for no. of channels
    if len(image.shape) == 3:
        # OpenCV represents images in BGR order; however PIL represents images in RGB order, so we need to swap the channels
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # convert the image to PIL format
    image = Image.fromarray(image)
    # resize the image
    image = image.resize(size)
    # convert the image (PIL format) to ImageTk format
    image = ImageTk.PhotoImage(image=image)
    # return TK image
    return image