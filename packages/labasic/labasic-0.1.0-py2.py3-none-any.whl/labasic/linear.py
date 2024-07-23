#Import libraries
import matplotlib.pyplot as plt
from scipy import stats
#Import data
profit = [1, 2, 3, 4, 5, 6]
population = [50, 100, 150, 40, 170, 90]
#Visualize the data
plt.figure()
plt.scatter(population, profit)
plt.xlabel("Population")
plt.ylabel("Profit")
plt.title("Data Visualization")
slope, intercept, r, p, std_err = stats.linregress(population, profit)
def linearRegression(x):
 return slope * x + intercept
LR = list(map(linearRegression, population))
print("LR Model Values:",LR)
plt.figure()
plt.scatter(population, profit)
plt.plot(population, LR)
plt.xlabel("Population")
plt.ylabel("Profit")
plt.title("Model Fit Line")
plt.show()
Newpop = 300
pf = linearRegression(Newpop)
print("The prediction of profit for 300 people is: ", pf)