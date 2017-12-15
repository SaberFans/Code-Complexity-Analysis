import matplotlib.pyplot as plt
workernum = [1,5,10,15,20]
time = [20.776124715805054,  8.15129017829895, 8.448184967041016, 10.523062467575073, 9.342151880264282 ]
plt.plot(workernum, time)
plt.xlabel('Worker numbers')
plt.ylabel('Time(s)')
plt.show()