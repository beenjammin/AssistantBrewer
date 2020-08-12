import matplotlib.pyplot as plt

times = [0,15,30,45,60]
temps = [65,55,60,75,20]

holdTemps = False
warmUp = False
tempTolerance = 5

tl = []
tl2 = []

for count, time in enumerate(times):
	#if both values are present
	if str(times[count]).isnumeric() and  str(temps[count]).isnumeric():     
		tl.append(times[count])
		tl2.append(temps[count])
print (tl)
print (tl2)


if holdTemps:
    plotTime = [tl[0]]
    plotTemp = [tl2[0]]
    for count in range(len(tl)):
    	#check to make sure it is not the first indice
    	if count is not 0:
    		#append a value just before
    		plotTime += [tl[count]-0.01,tl[count]]
    		plotTemp += [tl2[count-1],tl2[count]]
else:
    plotTime = tl
    plotTemp = tl2

try:
	tempToPlot = [[a - tempTolerance for a in plotTemp],[a + tempTolerance for a in plotTemp]]
except TypeError:
	tempToPlot = None
except:
	print("Unexpected error:", sys.exc_info()[0])
	raise
	
print (plotTime)
print (plotTemp)
print (tempToPlot)

fig, ax = plt.subplots(1)
ax.plot(plotTime, plotTemp, lw=2, label='Temperature Target', color='blue')
ax.fill_between(plotTime, tempToPlot[0], tempToPlot[1], facecolor='blue', alpha=0.25,
                label='Tolerance')
ax.set_xlabel('Time')
ax.set_ylabel('Temp (°C)')
ax.grid()
ax.legend(loc='upper left')
plt.show()