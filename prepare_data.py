import os
import sqlite3
import pandas as pd
from pathlib import Path

# Get the directory where this script is located
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "inventory.db"

def create_database():
    """Create and populate the inventory database from CSV or sample data."""
    
    # Sample inventory data
    data = {
        'product_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'name': [
            'Laptop Computer',
            'USB Cable',
            'Wireless Mouse',
            'Mechanical Keyboard',
            'Monitor Stand',
            'Power Adapter',
            'HDMI Cable',
            'Desk Lamp',
            'Phone Case',
            'Screen Protector'
        ],
        'category': [
            'Electronics',
            'Accessories',
            'Electronics',
            'Electronics',
            'Accessories',
            'Electronics',
            'Accessories',
            'Office Supplies',
            'Accessories',
            'Accessories'
        ],
        'quantity_in_stock': [5, 150, 32, 18, 25, 45, 200, 12, 85, 120],
        'unit_price': [1299.99, 9.99, 24.99, 89.99, 39.99, 49.99, 12.99, 34.99, 14.99, 8.99]
    }
    
    df = pd.DataFrame(data)
    
    # Create SQLite database
    conn = sqlite3.connect(DATABASE_PATH)
    df.to_sql('inventory', conn, if_exists='replace', index=False)
    conn.close()
    
    print(f"Database created successfully at: {DATABASE_PATH}")
    print(f"Total records: {len(df)}")
    print(df)

if __name__ == "__main__":
    create_database()
