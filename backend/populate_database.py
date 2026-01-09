import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values

# Load environment variables
load_dotenv()

# Training data
X = [[181, 80, 44], [177, 70, 43], [160, 60, 38], [154, 54, 37],
     [166, 65, 40], [190, 90, 47], [175, 64, 39], [177, 70, 40], [159, 55, 37],
     [171, 75, 42], [181, 85, 43]]

Y = ['male', 'female', 'female', 'female',
     'male', 'male', 'male', 'female', 'male',
     'female', 'male']


def populate_database():
    """Populate the Neon PostgreSQL database with training data"""

    database_url = os.getenv('DATABASE_URL')

    if not database_url:
        print("Error: DATABASE_URL not found in .env file")
        return

    try:
        # Connect to the database
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()

        print("Connected to Neon database successfully!")

        # Clear existing data
        print("Clearing existing data...")
        cursor.execute("DELETE FROM person_data;")
        conn.commit()

        # Prepare data for insertion
        data_to_insert = []
        for i in range(len(X)):
            height, weight, shoe_size = X[i]
            gender = Y[i]
            data_to_insert.append((height, weight, shoe_size, gender))

        # Insert training data
        print("Inserting training data...")
        insert_query = "INSERT INTO person_data (height, weight, shoe_size, gender) VALUES %s"
        execute_values(cursor, insert_query, data_to_insert)
        conn.commit()

        print(f"Successfully added {len(X)} records to the database!")

        # Verify the data
        cursor.execute("SELECT * FROM person_data;")
        all_records = cursor.fetchall()

        print(f"\nTotal records in database: {len(all_records)}")
        print("\nDatabase contents:")
        print("-" * 70)
        print(f"{'ID':<5} {'Height':<10} {'Weight':<10} {'Shoe Size':<12} {'Gender':<10}")
        print("-" * 70)
        for record in all_records:
            record_id, height, weight, shoe_size, gender = record
            print(f"{record_id:<5} {height:<10} {weight:<10} {shoe_size:<12} {gender:<10}")
        print("-" * 70)

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error connecting to or populating database: {e}")
        return


if __name__ == '__main__':
    populate_database()
    print("\nDatabase populated successfully!")