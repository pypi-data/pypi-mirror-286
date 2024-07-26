# steps/preprocess.py

import os
import pickle
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from modelhub.client import ModelHub

# Initialize the ModelHub client
modelhub_client = ModelHub(base_url="http://localhost:3000/api/v1")

# Get the MLflow client from ModelHub client
mlflow = modelhub_client.mlflow()

mlflow.set_experiment(experiment_id="9")

def preprocess_and_log_data():
    # Load the Iris dataset
    iris = load_iris()
    X = iris.data
    y = iris.target

    # Save the original dataset as a CSV file
    original_data = pd.DataFrame(X, columns=iris.feature_names)
    original_data['target'] = y
    original_data_csv = 'original_dataset.csv'
    original_data.to_csv(original_data_csv, index=False)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the scaler
    scaler = StandardScaler()

    # Fit and transform the training data
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Create DataFrames for the scaled data
    train_df = pd.DataFrame(X_train_scaled, columns=iris.feature_names)
    train_df['target'] = y_train
    test_df = pd.DataFrame(X_test_scaled, columns=iris.feature_names)
    test_df['target'] = y_test

    # Save the DataFrames to CSV files
    train_csv = 'train_preprocessed.csv'
    test_csv = 'test_preprocessed.csv'
    train_df.to_csv(train_csv, index=False)
    test_df.to_csv(test_csv, index=False)

    # Start an MLflow run
    with mlflow.start_run(run_name="preprocess"):
        try:
            # Log the parameters
            mlflow.log_param("random_state", 42)
            mlflow.log_param("test_size", 0.2)

            # Log the original dataset as an input
            eval_dataset_uri = mlflow.data.from_pandas(original_data, source="original_dataset.csv", name="Original Dataset")
            mlflow.log_input(eval_dataset_uri, context="preprocessing")

            # Log the scaler as an artifact
            scaler_path = 'scaler.pkl'
            with open(scaler_path, 'wb') as f:
                pickle.dump(scaler, f)
            mlflow.log_artifact(scaler_path, "preprocessing")

            # Log the preprocessed data as artifacts
            mlflow.log_artifact(train_csv, "data")
            mlflow.log_artifact(test_csv, "data")

            print("Preprocessing and logging complete")

        except Exception as e:
            print(f"An error occurred: {e}")
            mlflow.end_run(status=mlflow.entities.RunStatus.FAILED)
            raise

if __name__ == "__main__":
    preprocess_and_log_data()