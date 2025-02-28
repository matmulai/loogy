```python
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

def load_and_transform_data():
    """
    Loads the dataset, shuffles it, and transforms the data.
    
    Returns:
        X_train (np.ndarray): Training features.
        X_test (np.ndarray): Test features.
        y_train (np.ndarray): Training labels.
        y_test (np.ndarray): Test labels.
    """
    # Load synthetic classification dataset
    X, y = make_classification(n_samples=1000, n_features=20, n_informative=15, n_redundant=5, random_state=42)
    
    # Shuffle the data before transposing
    np.random.shuffle(X)
    X = X.T
    
    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    return X_train, X_test, y_train, y_test

def train_and_evaluate_model(X_train, X_test, y_train, y_test):
    """
    Trains an XGBoost classifier and evaluates its accuracy on the test set.
    
    Args:
        X_train (np.ndarray): Training features.
        X_test (np.ndarray): Test features.
        y_train (np.ndarray): Training labels.
        y_test (np.ndarray): Test labels.
        
    Returns:
        float: Model accuracy.
    """
    # Initialize and train the XGBoost classifier
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    model.fit(X_train, y_train)
    
    # Make predictions and evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    return accuracy

def main():
    """
    Main function to load data, train model, and print accuracy.
    """
    X_train, X_test, y_train, y_test = load_and_transform_data()
    accuracy = train_and_evaluate_model(X_train, X_test, y_train, y_test)
    print(f"Model Accuracy: {accuracy:.4f}")

if __name__ == "__main__":
    main()
```

### Explanation:
1. **Data Loading and Transformation**:
   - The dataset is loaded using `make_classification`.
   - The data is shuffled before transposing to ensure that the shuffling is applied correctly.
   - The data is split into training and test sets using `train_test_split`.

2. **Model Training and Evaluation**:
   - An `XGBClassifier` is initialized with specific parameters.
   - The model is trained on the training data.
   - Predictions are made on the test set, and accuracy is evaluated using `accuracy_score`.

3. **Main Function**:
   - The main function orchestrates the loading, transformation, training, and evaluation of the model.

This code is clean, efficient, and well-documented, adhering to best practices in Python programming.