# Importing necessary libraries
import pickle
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Loading the breast cancer dataset
data = load_breast_cancer()
X = data.data
y = data.target

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    random_state=42)

# Training a RandomForestClassifier model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluating the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Saving the trained model to a pickle file
model_filename = './cancer_diagnosis_model.pkl'
with open(model_filename, 'wb') as file:
    pickle.dump(model, file)

print(f"cancer diagnosis model accuracy: {accuracy}")
