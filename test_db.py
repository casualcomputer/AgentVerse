from src_py.database.database import get_db, init_db

def test_database():
    try:
        # Initialize the database
        init_db()
        
        # Try to get a database session
        with get_db() as db:
            print("Database connection successful!")
            return True
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_database() 