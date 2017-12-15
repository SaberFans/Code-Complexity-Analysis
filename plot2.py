import matplotlib.pyplot as plt
workernum = [1,5,10,15,20]
time = [21.14473867416382, 7.945691347122192, 8.802302598953247, 8.334894895553589, 8.381795644760132]
plt.plot(workernum, time)
plt.xlabel('Worker numbers')
plt.ylabel('Time(s)')
plt.show()