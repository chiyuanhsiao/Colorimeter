# Colorimeter
It's my final project of photoelectric experiment. The purpose is to measure the color information, such as RGB value, luminance and XYZ coordinates of CIE 1931 color space. 

## Usage
You can open this program by simply following below commands:
    
    pip install -r requirements.txt
    python3 color.py
        
After opening the program, a python Tkinter GUI will show up. The following operations:

1. Click "color" option from the menu bar, and choose "select image" to import your image. 
2. Rolling the scrollbar or moving your cursor to the area where you are interested in, the detail value about its color will show at the right column. 
3. You can lock the value by clicking one time at the main window.  Clicking one more time, the value will be unlocked. 
4. You can select the new image directly, and the old one will be closed. 
5. Finish the program by closing the window.

## Others
For the raw images, the program supports .dng files. You can change to other raw image format by modifying line 198 in color.py, or it will be seen as a normal image file. 
The raw image will be processed to sRGB color space as default. You can also change this setting by modifying line 220 in color.py
