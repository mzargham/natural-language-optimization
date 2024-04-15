from scaffold import *
import numpy as np
import openai
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer

def M(s, vectorizer):
    """ Converts string s to a feature vector. """
    return vectorizer.transform([s])

def approximate_interior_point_method(initial_seeds, theta, iterations, sample_size):
    vectorizer = CountVectorizer()
    vectorizer.fit(initial_seeds)  # Fit the vectorizer on initial seeds to define the vocabulary
    
    X = vectorizer.transform(initial_seeds)
    y = np.array([C(seed) for seed in initial_seeds])
    
    logistic_model = LogisticRegression()
    logistic_model.fit(X, y)  # Train logistic regression on initial data

    current_points = initial_seeds
    best_point = None
    best_loss = float('inf')

    for iteration in range(iterations):
        new_points = []
        for point in current_points:
            new_points.extend([G(point, theta) for _ in range(sample_size)])
        new_points = [point for point in new_points if point is not None]

        X_new = vectorizer.transform(new_points)
        feasible = logistic_model.predict(X_new)  # Use logistic model to predict feasibility
        losses = np.array([L(point) if feasible[i] else float('inf') for i, point in enumerate(new_points)])

        if any(feasible):
            min_loss_idx = np.argmin(losses)
            if losses[min_loss_idx] < best_loss:
                best_loss = losses[min_loss_idx]
                best_point = new_points[min_loss_idx]

        # Update model with new data
        X = vectorizer.transform(new_points)
        y = np.array([C(point) for point in new_points])
        logistic_model.fit(X, y)  # Retrain logistic regression on accumulated data

        current_points = new_points
        theta *= 0.95  # Cooling: reduce temperature

    return best_point, best_loss

def main():
    initial_seeds = ["Explore new methods in AI-driven financial models.", 
                     "Discuss cutting-edge technologies in sustainable energy."]
    theta = 0.7
    iterations = 10
    sample_size = 3

    best_point, best_loss = approximate_interior_point_method(initial_seeds, theta, iterations, sample_size)
    print(f"Best feasible point: {best_point}\nWith loss: {best_loss}")

if __name__ == "__main__":
    main()
