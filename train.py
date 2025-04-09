import pandas as pd
import pyarrow.dataset as ds
from surprise import SVD, Dataset, Reader, accuracy
from surprise.model_selection import train_test_split
import joblib

# Load ratings and movies
ratings = ds.dataset("data/cloud/ratings/", format="parquet").to_table().to_pandas()
movies = ds.dataset("data/cloud/movies/", format="parquet").to_table().to_pandas()

# Merge datasets using lowercase 'movieid'
merged_data = pd.merge(ratings, movies, on="movieid", how="inner")

# Drop unnecessary timestamp column (if present)
merged_data = merged_data.drop(columns=['timestamp'], errors='ignore')

# Optimize memory usage
merged_data["userid"] = merged_data["userid"].astype("category")
merged_data["movieid"] = merged_data["movieid"].astype("category")
merged_data = merged_data.drop(columns=['title'])  # Title not needed for training

# Prepare for training
reader = Reader(rating_scale=(0.5, 5.0))
data = Dataset.load_from_df(
    merged_data[["userid", "movieid", "rating"]],  # Use lowercase columns
    reader
)

# Train-test split
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

# Train model
model = SVD(n_factors=50, n_epochs=20)
model.fit(trainset)

# Evaluate
predictions = model.test(testset)
print("RMSE:", accuracy.rmse(predictions))

# Save model
joblib.dump(model, "movie_recommender.pkl")