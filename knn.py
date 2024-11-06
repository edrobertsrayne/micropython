import math
from collections import Counter


class KNNColorClassifier:
    def __init__(self, k=3, metric="euclidean", normalization="minmax"):
        """
        Initialize the KNN classifier

        Args:
            k (int): Number of neighbors to use for classification
            metric (str): Distance metric to use
            normalization (str): Normalization method to use. Options:
                - 'none': No normalization
                - 'minmax': Scale to range [0, 1]
                - 'standard': Standardize to mean=0, std=1
                - 'rgb255': Divide by 255 (for RGB values)
        """
        self.k = k
        self.metric = metric
        self.normalization = normalization
        self.X_train = []
        self.y_train = []

        # Initialize normalization parameters with default values
        self.min_vals = [0, 0, 0]  # One for each RGB channel
        self.max_vals = [255, 255, 255]  # One for each RGB channel
        self.means = [0, 0, 0]  # One for each RGB channel
        self.stds = [1, 1, 1]  # One for each RGB channel

        # Flag to track if normalization parameters have been computed
        self.is_fitted = False

    def _normalize_minmax(self, X):
        """Normalize features to range [0, 1]"""
        if not self.is_fitted:
            # Compute during training
            self.min_vals = [min(x[i] for x in X) for i in range(3)]
            self.max_vals = [max(x[i] for x in X) for i in range(3)]
            self.is_fitted = True

        normalized = []
        for color in X:
            norm_color = []
            for i, val in enumerate(color):
                denom = self.max_vals[i] - self.min_vals[i]
                if denom == 0:
                    norm_val = 0  # Handle case where min=max
                else:
                    norm_val = (val - self.min_vals[i]) / denom
                norm_color.append(norm_val)
            normalized.append(tuple(norm_color))

        return normalized

    def _normalize_standard(self, X):
        """Standardize features to mean=0, std=1"""
        if not self.is_fitted:
            # Compute during training
            self.means = [sum(x[i] for x in X) / len(X) for i in range(3)]
            self.stds = [
                math.sqrt(sum((x[i] - self.means[i]) ** 2 for x in X) / len(X))
                for i in range(3)
            ]
            self.is_fitted = True

        normalized = []
        for color in X:
            norm_color = []
            for i, val in enumerate(color):
                if self.stds[i] == 0:
                    norm_val = 0  # Handle case where std=0
                else:
                    norm_val = (val - self.means[i]) / self.stds[i]
                norm_color.append(norm_val)
            normalized.append(tuple(norm_color))

        return normalized

    def _normalize_rgb255(self, X):
        """Simple normalization by dividing RGB values by 255"""
        return [(r / 255, g / 255, b / 255) for r, g, b in X]

    def _normalize(self, X):
        """Apply selected normalization method"""
        if self.normalization == "none":
            return X
        elif self.normalization == "minmax":
            return self._normalize_minmax(X)
        elif self.normalization == "standard":
            return self._normalize_standard(X)
        elif self.normalization == "rgb255":
            return self._normalize_rgb255(X)
        else:
            raise ValueError(f"Unknown normalization method: {self.normalization}")

    def _euclidean_distance(self, color1, color2):
        """Standard Euclidean distance"""
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

    def _manhattan_distance(self, color1, color2):
        """Manhattan/city block distance"""
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        return abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)

    def _chebyshev_distance(self, color1, color2):
        """Chebyshev/chessboard distance"""
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        return max(abs(r1 - r2), abs(g1 - g2), abs(b1 - b2))

    def _get_distance(self, color1, color2):
        """Get distance between colors using selected metric"""
        distance_functions = {
            "euclidean": self._euclidean_distance,
            "manhattan": self._manhattan_distance,
            "chebyshev": self._chebyshev_distance,
        }

        if self.metric not in distance_functions:
            raise ValueError(f"Unknown distance metric: {self.metric}")

        return distance_functions[self.metric](color1, color2)

    def fit(self, X, y):
        """Train the classifier by storing the normalized training data"""
        self.is_fitted = False  # Reset fitted flag
        self.X_train = self._normalize(X)
        self.y_train = y

    def predict_single(self, color):
        """Predict the label for a single RGB color"""
        # Normalize the input color using parameters from training data
        normalized_color = self._normalize([color])[0]

        distances = []
        for train_color, train_label in zip(self.X_train, self.y_train):
            dist = self._get_distance(normalized_color, train_color)
            distances.append((dist, train_label))

        distances.sort(key=lambda x: x[0])
        k_nearest = distances[: self.k]

        k_nearest_labels = [label for _, label in k_nearest]
        most_common = Counter(k_nearest_labels).most_common(1)
        return most_common[0][0]

    def predict(self, X):
        """Predict labels for multiple RGB colors"""
        return [self.predict_single(color) for color in X]
