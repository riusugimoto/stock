import numpy as np
from utils import euclidean_dist_squared, plot2Dclusters


class KMeans:
    def __init__(self, X, k, plot=False, log=True):
        self.rng = np.random.default_rng()
        if X is not None:
            self.fit(X, k, plot=plot, log=log)

    def get_assignments(self, X):
        D2 = euclidean_dist_squared(X, self.w)
        # D2[np.isnan(D2)] = np.inf  # shouldn't be necessary tbh
        return np.argmin(D2, axis=1)

    def update_means(self, X, y):
        for k_i in range(self.k):
            matching = y == k_i
            if matching.any():
                self.w[k_i] = X[matching].mean(axis=0)

    def fit(self, X, k, plot=False, log=True, plot_fn=None):
        self.k = k
        n, self.d = X.shape
        assert n >= k

        self.w = w = self.rng.choice(X, k, replace=False)  # k by d
        y = np.zeros(n)
        changes = n

        while changes != 0:
            y_old = y
            y = self.get_assignments(X)
            changes = np.sum(y != y_old)

            self.update_means(X, y)

            if plot and self.d == 2:
                from matplotlib import pyplot as plt

                plot2Dclusters(X, y, w)
                plt.pause(1)
                plt.clf()

            if log:
                print(f"Changes: {changes:>7,}")

        if plot and self.d == 2:
            plot2Dclusters(
                X, y, w, filename=f"{plot_fn or type(self).__name__.lower()}.png"
            )

    def loss(self, X, y=None):
        w = self.w
        if y is None:
            y = self.get_assignments(X)

        loss = 0
        for i in range(X.shape[0]): 
            cluster_mean = self.w[y[i]] 
            dist = np.sum(X[i]-cluster_mean)**2
            loss += dist
            print(loss)
        
        return loss
 