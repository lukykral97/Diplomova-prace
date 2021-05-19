import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import numpy as np
import serial
import time
import os
import mpld3
from mpld3 import plugins

def heatmap2d(arr: np.ndarray):
    plt.imshow(arr, cmap='viridis')
    plt.colorbar()
    plt.show()


ser = serial.Serial()
ser.port = '\\.\COM3'
ser.baudrate = 115200
ser.timeout = 10 #specify timeout when using readline()
ser.open()
if ser.is_open==True:
	print("\nSériový port otevřen. Konfigurace:\n")
	print(ser, "\n") #print serial parameters
pocet = 0
pole = []
i = 0
###################################stará verze se záznamem obrázků
fileName= ("./Obrazky/obr1")
###################################prekreslovani obrazku pro web
#fileName= ("./Desktop/WEB/obrazky/obr1")


uloz = False
#plt.savefig(fileName, format="png")

while(True):
    #time.sleep(0.8)
    #fig = plt.figure()
    # ser_bytes = ser.readline()

    for radek in range(24):
        pocet = pocet + 1
        for sloupec in range(32):
            # if (pocet > 1):
            #     pole.append(line)
            #     pocet = 0
            ser_bytes = ser.readline()
            pole.append(float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8")))
            if (float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8")) > 25 and float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8")) < 200):
                uloz = True
    #print("pole", pole)

            #pole = (float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8")))
            #pole_r = append(pole,[[(float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8")))]],0)
    # for radek in range(8):
    #     for sloupec in range(8):
    #         #data = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))[radek, sloupec]
    #         #pole.append(data)
    #         pocet = pocet + 1
    #         if (radek == 8 and sloupec == 8):
    #             np.r_[pole,[[(float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8")))]]]
    #         else:
    #             pole.append(float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8")))
    # pole = np.arange(64).reshape(8, 8)
    # pole = arange(64)
    # pole = pole.reshape((1,64))
    # m = pole.shape[0]  #image row size
    # n = pole.shape[1]  #image column size
    #
    # p = 8     #block row size
    # q = 8     #block column size

    # block_array = []
    # previous_row = 0
    #
    # for row_block in range(blocks_per_row):
    #     ser_bytes = ser.readline()
    #     previous_row = row_block * p
    #     previous_column = 0
    #     for column_block in range(blocks_per_column):
    #         pole.append(float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8")))
    #         previous_column = column_block * q
    #         block = pole[previous_row:previous_row+p,previous_column:previous_column+q]
    #         block_array.append(block)
    #
    # block_array = array(block_array)

    #print(data.shape)

    import math
    from numpy import array
    a = array(pole)
    #print(a.shape)
    #a = np.arange(64)
    a = a.reshape((24,32))

    #fig, ax = plt.subplots()
    #plt.clf()
    #fig.clear()
    #plt.ion()
    plt.clf()
    plt.imshow(a)
    plt.colorbar()

    # handles, labels = ax.get_legend_handles_labels() # return lines and labels
    # interactive_legend = plugins.InteractiveLegendPlugin(zip(handles, ax.collections),
    #                                                      labels,
    #                                                      alpha_unsel=0.5,
    #                                                      alpha_over=1.5,
    #                                                      start_visible=True)
    # plugins.connect(fig, interactive_legend)
    # mpld3.show()

    ###########prekreslovani obrazku na web
    #plt.savefig("...WEB\obrazky\obr1.png")
    plt.savefig(fileName)


############################## ukladani obrazku do slozky
    # if(uloz):
    #     while os.path.exists('{}{:d}.png'.format(fileName, i)):
    #         i += 1
    #     plt.savefig('{}{:d}.png'.format(fileName, i))
    #     uloz = False





#    plt.savefig("./Obrazky/my_obr.png")
    #print("...")
    plt.pause(0.001)
    # ax = heatmap2d(a)
    # #plt.draw()
    # plt.pause(0.2)
    # plt.close()


    #fig.canvas.draw()
    #fig.canvas.draw()
    #fig.canvas.draw()
    #
    #fig.canvas.flush_events()
    #time.sleep(0.5)
    #time.sleep(1)
    pole = []
#import os
#print (os.getcwd())

#print(matice)
#with open('dataTEST.txt','w') as f:
#    k=repr(matice)
#    f.write(k)
