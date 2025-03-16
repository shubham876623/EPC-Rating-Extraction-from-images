import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

# Global connection variable
conn = None

def get_db_connection():
    """Establish a single persistent connection to the MS SQL database."""
    global conn
    if conn is None or conn.closed:
        server = os.getenv("SERVER")
        database = os.getenv("DATABASE")
        username = os.getenv("USER_NAME")
        password = os.getenv("PASSWORD") 
        driver = "ODBC Driver 17 for SQL Server"  

        conn_str = f"DRIVER={{{driver}}};SERVER={server},1433;DATABASE={database};UID={username};PWD={password}"
        
        try:
            conn = pyodbc.connect(conn_str, timeout=10)
            print("✅ Database connection established.")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            conn = None
    return conn

def fetch_image_urls():
    """Retrieve image URLs from the database where values are missing."""
    conn = get_db_connection()  # Ensure connection is active
    cursor = conn.cursor()

    cursor.execute("SELECT PropertyId, PropertyEPC , Rating FROM dbo.ExtractedProperties") 
    rows = cursor.fetchall()

    return rows

def update_database(update_data):
    """Batch update extracted values into MS SQL database."""
    conn = get_db_connection()  
    cursor = conn.cursor()

    update_query = """
        UPDATE dbo.ExtractedProperties 
        SET Rating = ?, CurrentScore = ?, PotentialScore = ?
        WHERE PropertyId = ?
    """

    update_values = (update_data[1], update_data[2], update_data[3], update_data[0]) 

    try:
        cursor.execute(update_query, update_values)
        conn.commit()
    
        print(f"✅ 1 record updated successfully for PropertyId {update_data[0]}!")

    except pyodbc.Error as e:
        print(f"❌ SQL Execution Error: {e}")

    finally:
        cursor.close()

def close_connection():
    """Close the database connection at the end of execution."""
    global conn
    if conn:
        conn.close()
        print("✅ Database connection closed.")