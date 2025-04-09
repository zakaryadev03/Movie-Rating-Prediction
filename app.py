from flask import Flask, request, jsonify
import joblib
import boto3
import os

app = Flask(__name__)

def download_model_from_s3():
    # Retrieve AWS credentials from environment variables
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_REGION', 'us-east-1')

    # Define the S3 bucket and key where your model is stored
    bucket_name = 'movielens-models'
    object_key = 'models/movie_recommender.pkl'
    
    # Create an S3 client
    s3 = boto3.client('s3',
                      region_name=aws_region,
                      aws_access_key_id=aws_access_key,
                      aws_secret_access_key=aws_secret_key)
    
    # Download the model file to local storage
    local_path = 'movie_recommender.pkl'
    s3.download_file(bucket_name, object_key, local_path)
    return local_path

# Download the latest model from S3 before loading it
model_path = download_model_from_s3()
model = joblib.load(model_path)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    user_id = int(data["user_id"])
    movie_id = int(data["movie_id"])
    prediction = model.predict(user_id, movie_id).est
    return jsonify({"predicted_rating": round(prediction, 1)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)