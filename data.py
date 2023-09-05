from numpy import np
import matplotlib.pyplot as plt

y = np.arange(len(category))
barWidth = 0.3
plt.barh(y - barWidth/2, frequency, barWidth, label=f"{dataset}")
plt.barh(y + barWidth/2, frequency2, barWidth, label=f"{dataset2}")

plt.xlabel('Frequency')
plt.ylabel(f'{featureType}')
plt.title(f'Top {categorySize} {featureType} from {dataset} Dataset Compared to {dataset2} Dataset ({sampleSize} samples)')
plt.yticks(y, category)
plt.legend()

plt.show()

