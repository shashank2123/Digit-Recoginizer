from tkinter import *
from tkinter import ttk, colorchooser, filedialog
from PIL import Image, ImageDraw
from tensorflow.keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray

class main:
    def __init__(self,master):
        self.master = master
        self.color_fg = 'black'
        self.color_bg = 'white'
        self.old_x = None
        self.old_y = None
        self.penwidth = 5
        self.drawWidgets()
        self.c.bind('<B1-Motion>',self.paint)
        self.c.bind('<Double-Button-1>',self.prediction)
        self.c.bind('<ButtonRelease-1>',self.reset)

    def paint(self,e):
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x,self.old_y,e.x,e.y,width=2,fill='black',capstyle=ROUND,smooth=True)
            self.draw.line([self.old_x,self.old_y,e.x,e.y],fill='black',width=2)
        self.old_x = e.x
        self.old_y = e.y

    def reset(self,e):
        self.old_x = None
        self.old_y = None
        
    def prediction(self,e):
        self.old_x = None
        self.old_y = None
        self.c.config(state=DISABLED)
        self.detect()
        self.c.config(state=NORMAL)
        self.c.delete(ALL)
        
        

    def detect(self):
        #img=self.im.resize((28,28),Image.ANTIALIAS)
        img=self.im
        img_data=np.asarray(img)
        gray_data=rgb2gray(img_data)
        model=load_model("mnist_digit.hdf5")
        result=model.predict_classes(gray_data.reshape(1,28,28,1))[0]
        #self.draw.rectangle([(0,0),(28,28)], fill = (255,255,255) )
        self.text.config(state=NORMAL)
        self.text.delete(1.0,END)
        self.text.insert(END,result)
        self.text.config(state=DISABLED)
        self.create_im()
        
        
            
           
    def clear(self):
        self.c.delete(ALL)
    
    def create_im(self):
        self.im=Image.new('RGB',(28,28),color=(255,255,255))
        self.draw=ImageDraw.Draw(self.im)


    def drawWidgets(self):
        self.controls = Frame(self.master,padx = 5,pady = 5)
        self.c = Canvas(self.master,bg='white',width=28,height=28)
        self.c.pack()
        self.create_im()
        menu = Menu(self.master)
        self.master.config(menu=menu)
        optionmenu = Menu(menu)
        menu.add_cascade(label='Options',menu=optionmenu)
        optionmenu.add_command(label='Clear Canvas',command=self.clear)
        optionmenu.add_command(label='Exit',command=self.master.destroy)
        self.text=Text(self.master,bg='black',fg='white',width=2,height=1,font=('Times','18','bold'))
        self.text.place(relx=0.43,rely=0.4)
        self.text.config(state=DISABLED)
        
        

if __name__ == '__main__':
    root = Tk()
    root.title('DrawingApp')
    root.geometry('200x200+500+100')
    root.maxsize(500,500)
    main(root)
    root.mainloop()