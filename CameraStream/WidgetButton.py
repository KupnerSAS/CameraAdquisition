import tkinter

class Display:
    def __init__(self):
        # Constructor
        self.root = tkinter.Tk()
        self.root.title('Parámetros')
        self.root.geometry('300x100')
        """     
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.label = tkinter.Label(self.root, text='column_1', font= 'Aerial 15 bold')
        self.label.grid(column=0, row=0)
        self.label.grid_columnconfigure(1, weight=1)
        self.label.grid_rowconfigure(1, weight=1)"""

        self.options = ['Continuous',
                        'Single Frame',
                        'Multi Frame']
        self.options_2 = ['Newest Only',
                          'Newest First',
                          'Oldest First',
                          'Oldeset First Overwrite']
        
        self.var = tkinter.StringVar(self.root)        
        self.var.set(self.options[0])
        self.var_2 = tkinter.StringVar(self.root)        
        self.var_2.set(self.options_2[0])
        
        # self.var.trace('w', self.change)

        self.dropDownMenu = tkinter.OptionMenu(self.root, self.var, *self.options)
        self.dropDownMenu.grid(column=0, columnspan=2, row=1)

        self.submit = tkinter.Button(self.root, text='Submit', command=lambda :self.show(self.var.get(), self.var_2.get()))
        self.submit.grid(column=2, row=1)

        self.send = tkinter.Button(self.root, text='Send data', command=self.send_data)
        self.send.grid(column=2, row=2)

        self.dropDownMenu_2 = tkinter.OptionMenu(self.root, self.var_2, *self.options_2)
        self.dropDownMenu_2.grid(column=0, columnspan=2, row=2)

        #self.video = VideoStream

        self.button = tkinter.Button(self.root, text='Get video')
        self.button.grid(column=2, row=3)

        #self.new_window = tkinter.Button(self.root, text='Get video', command=self.get_video)
        #self.new_window.grid(column=2, row=2)

        if __name__ == '__main__':
            self.root.mainloop()
        
    def show(self, value_1, value_2):
        print(f'Option: {value_1} and {value_2}')

    def send_data(self):
        last_var = self.var.get()
        last_var2 = self.var_2.get()
        print(last_var, last_var2)
        result = [f'Option: {last_var} and {last_var2}']
        return result


if __name__ == '__main__':
    display_1 = Display()

    
