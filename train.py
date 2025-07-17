from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
import pandas as pd
import re

# Load and preprocess dataset
df = pd.read_csv('data.csv', delimiter='|')
def preprocess(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text
df['review'] = df['review'].apply(preprocess)

X = df['review'].tolist()
y = df['rating'].tolist()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

embedder = SentenceTransformer('all-MiniLM-L6-v2')

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

# for name, model in models:
#     model.fit(X_train_vec, y_train)
#     y_pred = model.predict(X_test_vec)
    
#     print(f"{name} - Mean Absolute Error: {mean_absolute_error(y_test, y_pred)}")
#     print(f"{name} - Mean Squared Error: {mean_squared_error(y_test, y_pred)}")
#     print(f"{name} - R^2 Score: {r2_score(y_test, y_pred)}")
#     print(f"-" * 50)

X_train_vec = embedder.encode(X_train, convert_to_tensor=False)
X_test_vec = embedder.encode(X_test, convert_to_tensor=False)

regressor = VotingRegressor(estimators=[
    ('ridge', Ridge()),
    ('random_forest', RandomForestRegressor(n_estimators=100, random_state=42))
])

regressor.fit(X_train_vec, y_train)
y_pred = regressor.predict(X_test_vec)

print(f"Mean Absolute Error: {mean_absolute_error(y_test, y_pred)}")
print(f"Mean Squared Error: {mean_squared_error(y_test, y_pred)}")
print(f"R^2 Score: {r2_score(y_test, y_pred)}")

new_review = """Not many complaints, I didn't pay attention in class at all, but Dr. Maddux is chill enough to not care, plus she is a really great speaker. Class consists of her leading discussions with students about key concepts that she wants to communicate, and writing a reflection about the discussion that is automatically graded a 10/10. The projects for the class are kind of annoying though, you have to go out in the "Route One Corridor" 3 separate times and attend events, then make a poster about each one. Overall, you can put a minimal amount of effort into the class and get an A, and the content is decently interesting. I would recommend this professor and class."""
new_review_processed = preprocess(new_review)
new_review_vec = embedder.encode([new_review_processed])
predicted_rating = regressor.predict(new_review_vec)

print(f"Predicted rating for the new review: {predicted_rating[0]}")

