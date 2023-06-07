import nidaqmx
import random
import matplotlib.pyplot as plt
import numpy as np
from nidaqmx.constants import (TerminalConfiguration)
# from flask import Flask, Response, jsonify, render_template
import cv2

ch0 = nidaqmx.Task()
ch0.ai_channels.add_ai_voltage_chan("Dev1/ai0", min_val=0.0, max_val=10.0, terminal_config=TerminalConfiguration.DIFF)
ch1 = nidaqmx.Task()
ch1.ai_channels.add_ai_voltage_chan("Dev1/ai1", min_val=0.0, max_val=10.0, terminal_config=TerminalConfiguration.RSE)

threshold = 1.5
data = []
count = 0
while True:
    data0 = ch0.read()
    data1 = ch1.read()
    data.append([count/1000, data0, data1])
    count += 1
    val = np.array([round(data0, 4), round(data1, 4)])
    print(val)

    #k = cv2.waitKey(33)
    #if k == 27:  # Esc key to stop
    #    break

    if data0 < threshold:
        print("Threshold reached")
        break

ch0.stop()
ch0.close()
ch1.stop()
ch1.close()

data = np.array(data)
plt.plot(data[:, 0], data[:, 1])
plt.plot(data[:, 0], data[:, 2])
plt.xlabel('time')
plt.ylabel('Voltage')

# displaying the title
plt.title("Sensor Reading Voltage (Voltage divider)")
plt.savefig('plot.pdf')
plt.show()

