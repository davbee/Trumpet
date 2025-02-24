import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# target delivery rate
target: float = 150.0

# Load the data from flow.csv
data = pd.read_csv("flow.csv")

# filter data per time range for the second hour
data = data[(data["Time"] >= 58) & (data["Time"] <= 120)]

# convert time from minutes to hours
data["Time"] = data["Time"] / 60

# convert weight of water to mass by specific gravity (sg)
sg: float = 0.997
data["Mass"] = data["Weight"] / sg

# initialize max and min of delivery rates in observation window
maxi = []
mini = []

# calculation window because the sample rate is 2-minute
cw = [1, 2, 5, 10, 15]

# for-loop for calculate the rates
for i in cw:
    # rate = difference of time / difference of time
    rate = data["Mass"].diff(i) / data["Time"].diff(i)

    # create header name for rate
    header: str = "rate" + str(i*2).zfill(2)

    # set header name
    data[header] = rate

    # percentage max and min error from target
    maxi += [(rate.max() / target - 1) * 100]
    mini += [(rate.min() / target - 1) * 100]
    # maxi.append((rate.max() / target - 1) * 100)
    # mini.append((rate.min() / target - 1) * 100)

# observaton window [2, 4, 10, 20, 30]
ow = [i * 2 for i in cw]

# drop first two rows for the second hour
data = data.drop(index=data.index[:2])

# calculate mean delivery rate
meanrate = np.mean(data.iloc[:, 3])

# calculate % mean delivery rate error
datamean = [(i / target - 1.0) * 100 for i in [meanrate] * 5]

# Matplotlib for plotting the Trumpet Curve

# plot figure size
plt.figure(figsize=(9, 6))

# set x limit
plt.xlim(0, 35)
plt.ylim(-5, 5)

# Plot the mean line
plt.plot(ow, datamean, "o--k", label="Mean")

# Plot the trumpet curves for maxi and mini
plt.plot(ow, maxi, "o--r", label="Max")
plt.plot(ow, mini, "o--b", label="Min")

# # Fill the area between the bounds
plt.fill_between(
    ow, maxi, mini, color='gray', alpha=0.2, label='Trumpet Range')

# add values to markers
for i, txt in enumerate(maxi):
    plt.annotate(
        round(txt, 2),
        (ow[i], maxi[i]),
        textcoords="offset points",
        xytext=(6, 8),
        ha="center",
    )

for i, txt in enumerate(mini):
    plt.annotate(
        round(txt, 2),
        (ow[i], mini[i]),
        textcoords="offset points",
        xytext=(6, -12),
        ha="center",
    )

plt.annotate(
    round(datamean[0], 2),
    (ow[0], datamean[0]),
    textcoords="offset points",
    xytext=(6, 8),
    ha="center",
)

# Add labels and title
plt.xlabel('Observation Window, minutes')
plt.ylabel('Delivery Error, %')
plt.title('Trumpet Curve Plot')

# Add legend
plt.legend()

# show grid
plt.grid(True)

# Show the plot
plt.show()
