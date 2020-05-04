import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# color thresholds for red blue and green
lower_red = np.array([0,50,50])
upper_red = np.array([10,255,255])

lower_blue = np.array([115, 50, 50])
upper_blue = np.array([130,255,255])

lower_yellow = np.array([20,100,100])
upper_yellow = np.array([30,255,255])

lower_green = np.array([90,46,112])
upper_green = np.array([98,250,250])
    
color_codes = {"red": (0, 0, 255), "blue": (255,0,0), "green": (0, 255, 0), "yellow": (0, 255, 255), "black": (0, 0, 0)}

def main(args):

    #Empty list for recording the colors identified
    colors = list(range(1, 4))
    
    #These are the images that are passed in from the neural net
    images = ["i1.png", "i2.png", "i3.png"]

    #These are the 4 coordinates of each image
    x1 = [205, 237, 205]
    x2 = [236, 252, 236]
    y1 = [128, 114, 128]
    y2 = [162, 149, 162]

    #This for loop runs through all the images using the scan_color function which is defined later
    for i in range(len(images)):
    	colors[i] = scan_color(images[i], x1[i], x2[i], y1[i], y2[i])
    
    #Deletable code
    print colors[0]
    print colors[1]
    print colors[2]
    
    #This displays the color sequence 
    plot(colors)
    
def plot(scanned):
    #Uses the report template 
    report = cv2.imread('report.png')
    
    #Deletable code
    print scanned[0]
    print scanned[1]
    print scanned[2]
    print color_codes[scanned[2]]
    
    #Fills in the rectangle of the template with color that was scanned
    cv2.rectangle(report, (40, 200), (285, 450), color_codes[scanned[0]], thickness = -1)
    cv2.rectangle(report, (355, 200), (610, 450), color_codes[scanned[1]], thickness = -1)
    cv2.rectangle(report, (680, 200), (950, 450), color_codes[scanned[2]], thickness = -1)

    #Puts the name of the color in the box above the colors
    cv2.putText(report, scanned[0], (120,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2);
    cv2.putText(report, scanned[1], (450,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2);
    cv2.putText(report, scanned[2], (780,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2);
    
    #Makes a pop up window for the report 
    cv2.namedWindow('Scan the Code', cv2.WINDOW_NORMAL)
    cv2.moveWindow('Scan the Code', 200,650)
    cv2.resizeWindow('Scan the Code', 575,350)
    cv2.imshow("Scan the Code", report)
    cv2.waitKey(0)
               


def scan_color(image, x1, x2, y1, y2):

    #Read in the image data and changes the values from BGR to HSV
    img = cv2.imread(image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    #Records the color at the center of the given coordinates 
    color =  np.array(img[(y1+y2)/2, (x2+x1)/2])
   
    #Initialize the color indexes
    red = 0
    blue = 0
    green = 0
    yellow = 0

    #Configure threshold for each color
    lower_threshold = {"red": lower_red,"blue": lower_blue, "green": lower_green, "yellow": lower_yellow}
    upper_threshold = {"red": upper_red,"blue": upper_blue, "green": upper_green, "yellow": upper_yellow}
    
    #The for loop checks if color is within threshold of the set colors
    for clr in lower_threshold.keys():
        lower_color = lower_threshold[clr]
        upper_color = upper_threshold[clr]
        for i in range(3):
            if (color[i] >= lower_color[i] and color[i] <= upper_color[i]):
                if(clr == "red"):
                    red += 1
                elif (clr == "blue"):
                    blue += 1
                elif(clr =="green"):
                    green += 1
                elif(clr == "yellow"):
                    yellow += 1
    
    if(red == 3):
        return 'red'
    elif(blue == 3):
        return 'blue'
    elif(green == 3):
        return 'green'
    else:
        return 'yellow'


if __name__ == '__main__':
    main(sys.argv)
