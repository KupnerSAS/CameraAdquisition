from tkinter import *


class Display:
    def __init__(self, master):
        master.title('Slider')
        self.slider_1 = Scale(master,
                              from_=1000,
                              to=5000000,
                              orient=HORIZONTAL,
                              resolution=10000,
                              length=500,
                              cursor='hand2',
                              command=self.slider)
        self.slider_1.pack()

        self.exposure_data = 100
        self.exposure()
        """     
        self.button_3 = Button(master, text='Slider', command=self.slider)
        self.button_3.pack()"""

    def slider(self, value):
        print('slider executed')
        self.exposure_data = value
        self.exposure()

    def exposure(self):
        print('exposure executed')
        print(self.exposure_data)

    @staticmethod
    def test():
        print('test')


def main():
    root = Tk()
    Display(root)
    root.mainloop()
    Display.test()


if __name__ == '__main__':
    main()
