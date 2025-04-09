import csv

def find_row_by_ids(csv_file, user_id_column, movie_id_column):
    """
    Finds and prints a row in a CSV file based on both user ID and movie ID.
    
    Args:
        csv_file (str): Path to the CSV file
        user_id_column (str): Name of the column containing user IDs
        movie_id_column (str): Name of the column containing movie IDs
    """
    # Get the IDs to search for
    search_user_id = input(f"Enter the user ID (from column '{user_id_column}'): ").strip()
    search_movie_id = input(f"Enter the movie ID (from column '{movie_id_column}'): ").strip()
    
    found = False
    
    try:
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Print header
            print("\nColumn Headers:", reader.fieldnames)
            
            # Search for the matching row
            for row in reader:
                if row[user_id_column] == search_user_id and row[movie_id_column] == search_movie_id:
                    print("\nFound matching row:")
                    for key, value in row.items():
                        print(f"{key}: {value}")
                    found = True
                    break
            
            if not found:
                print(f"\nNo row found with user ID '{search_user_id}' and movie ID '{search_movie_id}'")
    
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage:
if __name__ == "__main__":
    # Replace these with your actual file path and column names
    csv_file_path = './data/ratings.csv'  # Update with your CSV file path
    user_id_column_name = 'userId'     # Update with your user ID column name
    movie_id_column_name = 'movieId'   # Update with your movie ID column name
    
    find_row_by_ids(csv_file_path, user_id_column_name, movie_id_column_name)