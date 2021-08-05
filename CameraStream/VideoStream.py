from tkinter import *
import tkinter
from PIL import Image
from PIL import ImageTk
import cv2

class Camera:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.color_change = True

        self.options = ['Continuous',
                        'Single Frame',
                        'Multi Frame']
        self.options_2 = ['Newest Only',
                          'Newest First',
                          'Oldest First',
                          'Oldeset First Overwrite']
        
        self.var = tkinter.StringVar(master)        
        self.var.set(self.options[0])
        self.var_2 = tkinter.StringVar(master)        
        self.var_2.set(self.options_2[0])

        self.dropDownMenu = tkinter.OptionMenu(master, self.var, *self.options)
        self.dropDownMenu.pack()
        
        self.dropDownMenu_2 = tkinter.OptionMenu(master, self.var_2, *self.options_2)
        self.dropDownMenu_2.pack()


        self.submit = tkinter.Button(master, text='Submit', command=lambda :self.show(self.var.get(), self.var_2.get()))
        self.submit.pack()
        
        self.video_stream = Label(master)
        self.video_stream.pack()

        self.button_1 = Button(master, text='Start video', command=self.start_video)
        self.button_1.pack()

        self.button_2 = Button(master, text='Close video', command=self.stop_video)
        self.button_2.pack()

        self.button_3 = Button(master, text='Color', command=self.change_1)
        self.button_3.pack()

        self.button_4 = Button(master, text='Color', command=self.change_2)
        self.button_4.pack()

        self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def start_video(self):
        self.stream_state = True
        self.get_image_from_camera()

    def stop_video(self):
        self.stream_state = False
        self.get_image_from_camera()

    def change_1(self):
        self.color_change = True

    def change_2(self):
        self.color_change = False

    def show(self, value_1, value_2):
        print(f'Option: {value_1} and {value_2}')


    def get_image_from_camera(self):
        if self.stream_state:
            _, frame = self.camera.read()
            if self.color_change:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)             
            else:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(frame)

            self.video_stream.configure(image = frame)
            self.video_stream.image = frame
            self.video_stream.after(1, self.get_image_from_camera)


def main():
    root = Tk()
    
    Camera(root)

    root.mainloop()

if __name__ == "__main__":
    main()
