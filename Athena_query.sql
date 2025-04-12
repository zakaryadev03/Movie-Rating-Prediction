-- This view calculates the average rating and number of ratings for each movie
-- in the movielens_cleaned_db database, filtering out movies with fewer than 10 ratings.
CREATE OR REPLACE VIEW ratings_view AS 
SELECT 
  m.movieid,
  m.title,
  ROUND(AVG(r.rating), 2) AS avg_rating,
  COUNT(*) AS num_ratings
FROM movielens_cleaned_db.ratings r
JOIN movielens_cleaned_db.movies m ON r.movieid = m.movieid
GROUP BY m.movieid, m.title
HAVING COUNT(*) > 10;