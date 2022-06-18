import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import platform
import rawpy

class ScrollableImage(tk.Frame):
    def __init__(self, master=None, **kw):
        self.image = kw.pop('image', None)
        sw = kw.pop('scrollbarwidth', 10)
        super(ScrollableImage, self).__init__(master=master, **kw)
        self.cnvs = tk.Canvas(self, highlightthickness=0, **kw)
        self.cnvs.create_image(0, 0, anchor='nw', image=self.image)
        # Vertical and Horizontal scrollbars
        self.v_scroll = tk.Scrollbar(self, orient='vertical', width=sw)
        self.h_scroll = tk.Scrollbar(self, orient='horizontal', width=sw)
        # Grid and configure weight.
        self.cnvs.grid(row=0, column=0, sticky='nsew')
        self.h_scroll.grid(row=1, column=0, sticky='ew')
        self.v_scroll.grid(row=0, column=1, sticky='ns')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # Set the scrollbars to the canvas
        self.cnvs.config(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)
        # Set canvas view to the scrollbars
        self.v_scroll.config(command=self.cnvs.yview)
        self.h_scroll.config(command=self.cnvs.xview)
        # Assign the region to be scrolled
        self.cnvs.config(scrollregion=self.cnvs.bbox('all'), cursor="circle")
        self.cnvs.bind_class(self.cnvs, "<MouseWheel>", self.mouse_scroll)

    def mouse_scroll(self, event):
        if event.state == 0 :
            self.cnvs.yview_scroll(-1*(event.delta), 'units') # For MacOS
            self.cnvs.yview_scroll(int(-1*(event.delta/120)), 'units') # For windows
        if event.state == 1:
            self.cnvs.xview_scroll(-1*(event.delta), 'units') # For MacOS
            self.cnvs.xview_scroll(int(-1*(event.delta/120)), 'units') # For windows
            
    def printcoord(self, event):
        x, y = event.x, event.y
        print('Image pixel {}, {}'.format(x + int(self.image.width() * self.h_scroll.get()[0]), y + int(self.image.height() * self.v_scroll.get()[0])))
        
    def coordinate(self, event):
        return event.x + int(self.image.width() * self.h_scroll.get()[0]) + 1, event.y + int(self.image.height() * self.v_scroll.get()[0]) + 1
        
    def change_image(self, image):
        self.image = image
        self.cnvs.delete("all")
        self.cnvs.create_image(0, 0, anchor='nw', image=self.image)
        self.cnvs.config(scrollregion=self.cnvs.bbox('all'), cursor="circle")

class StatusColumn(tk.Frame):
    def __init__(self, master=None, **kw):
        self.image_window = kw.pop('image_window', None)
        self.PIL_image = kw.pop('PIL_image', None)
        super(StatusColumn, self).__init__(master=master, **kw)
        
        self.coordinate = tk.LabelFrame(self, text="Pixel Coordinate", padx=12, pady=6)
        self.x_coord_var = tk.StringVar()
        self.x_coord_var.set("x: 0")
        self.x_coord = tk.Entry(self.coordinate, textvariable=self.x_coord_var, cursor='xterm', state='readonly')
        self.x_coord.grid(row=0, column=0, sticky='nw')
        self.y_coord_var = tk.StringVar()
        self.y_coord_var.set("y: 0")
        self.y_coord = tk.Entry(self.coordinate, textvariable=self.y_coord_var, cursor='xterm', state='readonly')
        self.y_coord.grid(row=1, column=0, sticky='nw')
        self.coordinate.grid(row=1, column=0, sticky='ew')
        
        self.RGB = tk.LabelFrame(self, text="sRGB", padx=12, pady=6)
        self.R_var = tk.StringVar()
        self.R_var.set("R: None")
        self.R = tk.Entry(self.RGB, textvariable=self.R_var, cursor='xterm', state='readonly')
        self.R.grid(row=0, column=0, sticky='nw')
        self.G_var = tk.StringVar()
        self.G_var.set("G: None")
        self.G = tk.Entry(self.RGB, textvariable=self.G_var, cursor='xterm', state='readonly')
        self.G.grid(row=1, column=0, sticky='nw')
        self.B_var = tk.StringVar()
        self.B_var.set("B: None")
        self.B = tk.Entry(self.RGB, textvariable=self.B_var, cursor='xterm', state='readonly')
        self.B.grid(row=2, column=0, sticky='nw')
        self.RGB.grid(row=2, column=0, sticky='ew')
        
        self.XYZ = tk.LabelFrame(self, text="CIE XYZ", padx=12, pady=6)
        self.X_var = tk.StringVar()
        self.X_var.set("X: None")
        self.X = tk.Entry(self.XYZ, textvariable=self.X_var, cursor='xterm', state='readonly')
        self.X.grid(row=0, column=0, sticky='nw')
        self.Y_var = tk.StringVar()
        self.Y_var.set("Y: None")
        self.Y = tk.Entry(self.XYZ, textvariable=self.Y_var, cursor='xterm', state='readonly')
        self.Y.grid(row=1, column=0, sticky='nw')
        self.Z_var = tk.StringVar()
        self.Z_var.set("Z: None")
        self.Z = tk.Entry(self.XYZ, textvariable=self.Z_var, cursor='xterm', state='readonly')
        self.Z.grid(row=2, column=0, sticky='nw')
        self.x_var = tk.StringVar()
        self.x_var.set("x: None")
        self.x = tk.Entry(self.XYZ, textvariable=self.x_var, cursor='xterm', state='readonly')
        self.x.grid(row=3, column=0, sticky='nw')
        self.y_var = tk.StringVar()
        self.y_var.set("y: None")
        self.y = tk.Entry(self.XYZ, textvariable=self.y_var, cursor='xterm', state='readonly')
        self.y.grid(row=4, column=0, sticky='nw')
        self.z_var = tk.StringVar()
        self.z_var.set("z: None")
        self.z = tk.Entry(self.XYZ, textvariable=self.z_var, cursor='xterm', state='readonly')
        self.z.grid(row=5, column=0, sticky='nw')
        self.XYZ.grid(row=3, column=0, sticky='ew')
        
        #self.status = tk.StringVar()
        #self.status.set(f"Coordinate \n\tx: {0} \n\ty: {0} \n\nRGB \n\tr: {0} \n\tg: {0} \n\tb: {0} \n\nCIE1931 \n\tY: {0} \n\tx: {0} \n\ty: {0}")
        #self.label = tk.Label(self, textvariable=self.status)
        #self.label.grid(row=1, column=0, sticky='w')
        self.image_window.cnvs.bind("<Motion>", self.status_value_update)
        self.image_window.cnvs.bind("<ButtonPress-1>", self.switch_update)
        self.switch = 1
        
        self.colourchart = ColourChart(self)
        self.colourchart.canvas.grid(row=0, column=0, sticky='nw')

    def status_value_update(self, event):
        if (self.image_window.image != None):
            if (self.switch > 0):
                x_coord, y_coord = self.image_window.coordinate(event)
                if (x_coord >= 0 and x_coord < self.image_window.image.width() and y_coord >= 0 and y_coord < self.image_window.image.height()):
                    r, g, b = self.PIL_image.getpixel((x_coord, y_coord))
                    X, Y, Z, x, y, z = RGBtoXYZ(r, g, b)
                    self.colourchart.move(x, y)
                    #self.status.set(f"Coordinate \n\tx: {x_coord} \n\ty: {y_coord} \n\nRGB \n\tr: {r} \n\tg: {g} \n\tb: {b} \n\nCIE1931 \n\tY: {round(Y, 2)} \n\tx: {round(x, 4)} \n\ty: {round(y, 4)}")
                    self.x_coord_var.set(f"x: {x_coord}")
                    self.y_coord_var.set(f"y: {y_coord}")
                    self.R_var.set(f"R: {r}")
                    self.G_var.set(f"G: {g}")
                    self.B_var.set(f"B: {b}")
                    self.X_var.set(f"X: {round(X, 2)}")
                    self.Y_var.set(f"Y: {round(Y, 2)}")
                    self.Z_var.set(f"Z: {round(Z, 2)}")
                    self.x_var.set(f"x: {round(x, 4)}")
                    self.y_var.set(f"y: {round(y, 4)}")
                    self.z_var.set(f"z: {round(z, 4)}")
                else:
                    #self.status.set(f"Coordinate \n\tx: {x_coord} \n\ty: {y_coord} \n\nRGB \n\tr: fault \n\tg: fault \n\tb: fault \n\nCIE1931 \n\tY: fault \n\tx: fault \n\ty: fault")
                    self.x_coord_var.set(f"x: {x_coord}")
                    self.y_coord_var.set(f"y: {y_coord}")
                    self.R_var.set(f"R: out of range")
                    self.G_var.set(f"G: out of range")
                    self.B_var.set(f"B: out of range")
                    self.X_var.set(f"X: out of range")
                    self.Y_var.set(f"Y: out of range")
                    self.Z_var.set(f"Z: out of range")
                    self.x_var.set(f"x: out of range")
                    self.y_var.set(f"y: out of range")
                    self.z_var.set(f"z: out of range")
        else:
            #self.status.set(f"Coordinate \n\tx: {event.x} \n\ty: {event.y} \n\nRGB \n\tr: {0} \n\tg: {0} \n\tb: {0} \n\nCIE1931 \n\tY: {0} \n\tx: {0} \n\ty: {0}")
            self.x_coord_var.set(f"x: {event.x}")
            self.y_coord_var.set(f"y: {event.y}")
            self.R_var.set(f"R: None")
            self.G_var.set(f"G: None")
            self.B_var.set(f"B: None")
            self.X_var.set(f"X: None")
            self.Y_var.set(f"Y: None")
            self.Z_var.set(f"Z: None")
            self.x_var.set(f"x: None")
            self.y_var.set(f"y: None")
            self.z_var.set(f"z: None")
        
    def change_image(self, image):
        self.PIL_image = image
        self.PIL_image.convert('RGB')
        
    def switch_update(self, event):
        if (self.image_window.image != None):
            self.switch *= -1

class MenuBar():
    def __init__(self, root, **kw):
        self.root = root
        self.image_window = kw.pop('image_window', None)
        self.status_column = kw.pop('status_column', None)
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        self.menu = tk.Menu(self.menubar)
        self.menu.add_command(label="select image", command=self.select_image)
        self.menubar.add_cascade(label="color", menu=self.menu)
        self.PIL_image = None
        self.tkimage = None
        
    def select_image(self):
        if (platform.system() != 'Windows'):
            path = filedialog.askopenfilename(initialdir="/", title="Select Image")
        else:
            path = filedialog.askopenfilename(initialdir="C:/", title="Select Image")
        if (self.PIL_image != None):
            self.PIL_image.close()
        if (path[-3:] == 'dng'):
            self.PIL_image = OpenRaw(path)
        else:
            self.PIL_image = Image.open(path)
        self.tkimage = ImageTk.PhotoImage(self.PIL_image)
        self.image_window.change_image(self.tkimage)
        self.status_column.change_image(self.PIL_image)

class ColourChart():
    def __init__(self, root):
        self.root = root
        self.im = Image.open("./CIE1931xy_blank.png").resize((652 // 3, 693 // 3))
        self.colourchart = ImageTk.PhotoImage(self.im)
        self.canvas = tk.Canvas(self.root, width=self.im.size[0], height=self.im.size[1])
        self.canvas.create_image(0, 0, anchor='nw', image=self.colourchart)
        self.cursor = self.canvas.create_oval(93, 129, 103, 139)
        
    def move(self, x, y):
        self.canvas.moveto(self.cursor, 20 + 220 * x, 231 - 28 - 220 * y)
        
def OpenRaw(path):
    raw = rawpy.imread(path)
    a = raw.postprocess(output_color=rawpy.ColorSpace.sRGB, no_auto_bright=True)
    return Image.fromarray(a, mode='RGB')

def RGBtoXYZ(R, G, B):
    R /= 255
    G /= 255
    B /= 255
    R = tolinear(R)
    G = tolinear(G)
    B = tolinear(B)
    X = (0.4124564 * R + 0.3575761 * G + 0.1804375 * B) * 100
    Y = (0.2126729 * R + 0.7151522 * G + 0.0721750 * B) * 100
    Z = (0.0193339 * R + 0.1191920 * G + 0.9503041 * B) * 100
    if (X + Y + Z != 0):
        x = X / (X + Y + Z)
        y = Y / (X + Y + Z)
        z = Z / (X + Y + Z)
    else:
        x = 1 / 3
        y = 1 / 3
        z = 1 / 3
    return X, Y, Z, x, y, z
    
def tolinear(k):
    if k > 0.04045:
        return ((k + 0.055) / 1.055) ** 2.4
    else:
        return k / 12.92

def main():
    root = tk.Tk()
    root.title("Color")
    
    image_window = ScrollableImage(root, image=None, scrollbarwidth=6, width=900, height=600)
    image_window.grid(row=0, column=0, sticky='nsew')

    status_column = StatusColumn(root, image_window=image_window, PIL_image=None)
    status_column.grid(row=0, column=1, sticky='ns')

    menubar = MenuBar(root, image_window=image_window, status_column=status_column)

    root.mainloop()

if __name__ == '__main__':
    main()
