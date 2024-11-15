import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, f1_score, log_loss
from sklearn.preprocessing import LabelEncoder
import joblib

# Load the dataset
data = pd.read_csv("D:/College Work/AI/Obesity/Obesity_dataset.csv")

# Drop duplicate rows
data.drop_duplicates(inplace=True)

# Check for missing values
if data.isnull().sum().any():
    data.dropna(inplace=True)

# Check for duplicate columns
duplicate_columns = data.columns[data.columns.duplicated()]
if duplicate_columns.any():
    data.drop(columns=duplicate_columns, inplace=True)

# Encode categorical columns if necessary
label_encoders = {}
for column in data.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le

# Display the first few rows of the dataset
print(data.head())

# Separate features and target
X = data.drop('NObeyesdad', axis=1)  # Assuming 'NObeyesdad' is the target column
y = data['NObeyesdad']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Classifier
model = RandomForestClassifier(random_state=42)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')
logloss = log_loss(y_test, y_pred_proba)

print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")
print(f"Log Loss: {logloss:.2f}")
print("\nClassification Report:\n", classification_report(y_test, y_pred))

joblib.dump(model, 'rf_model.joblib')
joblib.dump(label_encoders, 'label_encoders.joblib')

# Load the model and label encoders
model = joblib.load('rf_model.joblib')
label_encoders = joblib.load('label_encoders.joblib')

# Save label encoders for reference
for column, le in label_encoders.items():
    print(f"Encoding for {column}: {dict(zip(le.classes_, le.transform(le.classes_)))}")

# Function to get input from the user and predict
def predict_obesity():
    user_data = {}
    for col in X.columns:
        # Check if column is categorical
        if col in label_encoders:
            categories = label_encoders[col].classes_
            print(f"\nChoose an option for {col} (Categories: {', '.join(categories)}):")
            for i, cat in enumerate(categories):
                print(f"{i}: {cat}")
            user_input = int(input(f"Enter the number corresponding to your choice for {col}: "))
            user_data[col] = user_input
        else:
            user_data[col] = float(input(f"Enter value for {col}: "))

    # Convert user input to DataFrame for prediction
    input_df = pd.DataFrame([user_data])

    # Predict the class
    prediction = model.predict(input_df)[0]
    # Convert prediction back to original label if necessary
    predicted_label = label_encoders['NObeyesdad'].inverse_transform([prediction])[0]
    print(f"\nPredicted Obesity Classification: {predicted_label}")

# Call the prediction function
predict_obesity()

# Save the model
joblib.dump(model, "obesity_random_forest_model.pkl")

# Save the label encoders
joblib.dump(label_encoders, "label_encoders.pkl")

# Load the model and label encoders
model = joblib.load("obesity_random_forest_model.pkl")
label_encoders = joblib.load("label_encoders.pkl")
