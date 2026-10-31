
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 1. Load the email dataset
print("Loading email dataset...")

df = pd.read_csv("dataset/phishing_email.csv")

# 2. Remove rows with missing email text or labels
df = df.dropna(subset=["text_combined", "label"])

# 3. Prepare the email text and labels
X = df["text_combined"].astype(str)
y = df["label"].astype(int)

print("Dataset loaded successfully!")
print("Total emails:", len(df))
print("Label distribution:")
print(y.value_counts())

# 4. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 5. Build the machine-learning pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        max_features=50000,
        ngram_range=(1, 2)
    )),
    ("classifier", LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ))
])

# 6. Train the model
print("\nTraining the AI model...")
model.fit(X_train, y_train)

# 7. Test the model
print("\nTesting the model...")

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")
print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

# 8. Save the trained model
joblib.dump(model, "model/phishing_model.pkl")

print("\nModel saved successfully!")
print("Location: model/phishing_model.pkl")
