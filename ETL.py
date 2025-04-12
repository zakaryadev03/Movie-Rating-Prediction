from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark.sql.functions import col, regexp_extract, when, lit
#This script is for AWS Glue ETL job
# Initialize
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Load data
ratings = glueContext.create_dynamic_frame.from_catalog(
    database="movielens_db", 
    table_name="ratings_csv"
).toDF()

movies = glueContext.create_dynamic_frame.from_catalog(
    database="movielens_db", 
    table_name="movies_csv"
).toDF()

# --- Data Cleaning (Same as Before) ---
ratings = ratings.dropDuplicates(["userid", "movieid"])
# ... (keep your existing filtering steps) ...

# --- Feature Engineering ---
# 1. Extract year from title
movies = movies.withColumn("year", regexp_extract(col("title"), r"\((\d{4})\)", 1).cast("int"))

# 2. Handle "no genres listed" by replacing with "Unknown"
movies = movies.withColumn(
    "genres", 
    when(col("genres") == "(no genres listed)", "Unknown").otherwise(col("genres"))
)

# 3. One-hot encode ALL genres dynamically
genres_list = [
    'Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy', 
    'Romance', 'Drama', 'Action', 'Crime', 'Thriller', 
    'Horror', 'Mystery', 'Sci-Fi', 'IMAX', 'Documentary', 
    'War', 'Musical', 'Western', 'Film-Noir', 'Unknown'
]

for genre in genres_list:
    movies = movies.withColumn(
        f"genre_{genre.lower().replace('-', '_')}",  # e.g., "Sci-Fi" -> "genre_sci_fi"
        when(col("genres").contains(genre), 1).otherwise(0)
    )

# 4. Drop the original "genres" column
movies = movies.drop("genres")

# --- Save to S3 (Same as Before) ---
cleaned_path = "s3://movielens-raw-data/cleaned_data/"
ratings.write.mode("overwrite").parquet(f"{cleaned_path}ratings")
movies.write.mode("overwrite").parquet(f"{cleaned_path}movies")