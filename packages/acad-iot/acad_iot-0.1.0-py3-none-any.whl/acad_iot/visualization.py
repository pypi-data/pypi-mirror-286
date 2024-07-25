import matplotlib.pyplot as plt
import seaborn as sns

class Visualizer:
    def __init__(self):
        sns.set(style="whitegrid")
    
    def plot_clusters(self, X, labels):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=X[:, 0], y=X[:, 1], hue=labels, palette="viridis")
        plt.title("Cluster Visualization")
        plt.show()
    
    def plot_anomalies(self, X, anomaly_scores, threshold=0):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=X[:, 0], y=X[:, 1], hue=anomaly_scores > threshold, palette="viridis")
        plt.title("Anomaly Detection")
        plt.show()
