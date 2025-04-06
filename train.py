from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import re

# Load and preprocess dataset
df = pd.read_csv('data.csv', delimiter='|')
def preprocess(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text
df['review'] = df['review'].apply(preprocess)

X = df['review']
y = df['rating']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize text data
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Models
# models = [
#     ('Ridge', Ridge()),
#     ('Lasso', Lasso()),
#     ('ElasticNet', ElasticNet()),
#     ('RandomForest', RandomForestRegressor(n_estimators=100, random_state=42)),
#     ('GradientBoosting', GradientBoostingRegressor(n_estimators=100, random_state=42)),
#     ('SVR', SVR()),
#     ('KNN', KNeighborsRegressor(n_neighbors=5)),
#     ('VotingRegressor', VotingRegressor(estimators=[('ridge', Ridge()), ('random_forest', RandomForestRegressor())]))
# ]

# # Train and evaluate models
# for name, model in models:
#     model.fit(X_train_vec, y_train)
#     y_pred = model.predict(X_test_vec)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_vec, y_train)
y_pred = model.predict(X_test_vec)

print(f"Mean Absolute Error: {mean_absolute_error(y_test, y_pred)}")
print(f"Mean Squared Error: {mean_squared_error(y_test, y_pred)}")
print(f"R^2 Score: {r2_score(y_test, y_pred)}")

# Example of a new review
new_review = "I recommend this professor. They are very helpful and knowledgeable."

# Preprocess the new review (same as done for training data)
new_review_processed = preprocess(new_review)

# Vectorize the new review using the same vectorizer as during training
new_review_vec = vectorizer.transform([new_review_processed])

# Predict the rating for the new review
predicted_rating = model.predict(new_review_vec)

print(f"Predicted rating for the new review: {predicted_rating[0]}")

