"""
Run this ONCE to create the products database.
Command: python init_db.py
"""
import sqlite3
import os

DB_PATH = os.path.join("data", "products.db")
os.makedirs("data", exist_ok=True)

PRODUCTS = [
    # Electronics - Phones
    ("P001", "iPhone 15 128GB",        "Electronics", "Glass & Aluminum", "One Size", "Black",        "Apple",    "Unisex", 25, 79999.0),
    ("P002", "iPhone 15 128GB",        "Electronics", "Glass & Aluminum", "One Size", "White",        "Apple",    "Unisex", 18, 79999.0),
    ("P003", "iPhone 15 128GB",        "Electronics", "Glass & Aluminum", "One Size", "Pink",         "Apple",    "Unisex", 12, 79999.0),
    ("P004", "Samsung Galaxy S24",     "Electronics", "Gorilla Glass",    "One Size", "Black",        "Samsung",  "Unisex", 30, 69999.0),
    ("P005", "Samsung Galaxy S24",     "Electronics", "Gorilla Glass",    "One Size", "Violet",       "Samsung",  "Unisex", 20, 69999.0),
    ("P006", "Redmi Note 13 Pro",      "Electronics", "Plastic & Glass",  "One Size", "Midnight Black","Xiaomi",  "Unisex", 50, 24999.0),
    ("P007", "Redmi Note 13 Pro",      "Electronics", "Plastic & Glass",  "One Size", "Arctic White", "Xiaomi",   "Unisex", 45, 24999.0),
    ("P008", "OnePlus Nord CE 4",      "Electronics", "Glass & Plastic",  "One Size", "Celadon Marble","OnePlus", "Unisex", 35, 24999.0),
    ("P009", "Realme 12 Pro+",         "Electronics", "Plastic & Glass",  "One Size", "Navigator Beige","Realme", "Unisex", 40, 29999.0),
    # Electronics - Laptops
    ("P010", "HP Pavilion 15",         "Electronics", "Core i5, 16GB RAM, 512GB SSD", "15.6 inch", "Silver", "HP",  "Unisex", 15, 58990.0),
    ("P011", "Dell Inspiron 15",       "Electronics", "Core i7, 16GB RAM, 1TB SSD",   "15.6 inch", "Black",  "Dell","Unisex", 10, 75990.0),
    ("P012", "Lenovo IdeaPad Slim 3",  "Electronics", "Core i5, 8GB RAM, 512GB SSD",  "15.6 inch", "Arctic Grey","Lenovo","Unisex",20,42990.0),
    ("P013", "ASUS VivoBook 15",       "Electronics", "Core i3, 8GB RAM, 256GB SSD",  "15.6 inch", "Transparent Silver","ASUS","Unisex",18,34990.0),
    # Electronics - Audio
    ("P014", "Sony WH-1000XM5",        "Electronics", "Plastic & Metal",  "One Size", "Black",        "Sony",     "Unisex", 22, 29990.0),
    ("P015", "Sony WH-1000XM5",        "Electronics", "Plastic & Metal",  "One Size", "Silver",       "Sony",     "Unisex", 15, 29990.0),
    ("P016", "Boat Rockerz 450",       "Electronics", "Plastic",          "One Size", "Black",        "boAt",     "Unisex", 60, 1299.0),
    ("P017", "Boat Rockerz 450",       "Electronics", "Plastic",          "One Size", "Blue",         "boAt",     "Unisex", 55, 1299.0),
    ("P018", "JBL Tune 510BT",         "Electronics", "Plastic",          "One Size", "Black",        "JBL",      "Unisex", 30, 2499.0),
    ("P019", "Boat Airdopes 141",      "Electronics", "Plastic",          "One Size", "Active Black", "boAt",     "Unisex", 80, 999.0),
    # Electronics - Watches
    ("P020", "Apple Watch Series 9 41mm","Electronics","Aluminium",       "41mm",     "Midnight",     "Apple",    "Unisex", 12, 41900.0),
    ("P021", "Apple Watch Series 9 45mm","Electronics","Aluminium",       "45mm",     "Starlight",    "Apple",    "Unisex", 10, 44900.0),
    ("P022", "Samsung Galaxy Watch 6", "Electronics", "Aluminium",        "44mm",     "Graphite",     "Samsung",  "Unisex", 18, 26999.0),
    ("P023", "Noise ColorFit Pro 4",   "Electronics", "Aluminium",        "One Size", "Jet Black",    "Noise",    "Unisex", 40, 2499.0),
    # Clothing - Men
    ("P024", "Levi's 511 Slim Fit Jeans","Clothing",  "100% Cotton Denim","28,30,32,34,36","Blue",    "Levi's",   "Male",   45, 3499.0),
    ("P025", "Levi's 511 Slim Fit Jeans","Clothing",  "100% Cotton Denim","28,30,32,34,36","Black",   "Levi's",   "Male",   40, 3499.0),
    ("P026", "Allen Solly Formal Shirt","Clothing",   "60% Cotton 40% Polyester","S,M,L,XL,XXL","White","Allen Solly","Male",30,1499.0),
    ("P027", "Allen Solly Formal Shirt","Clothing",   "60% Cotton 40% Polyester","S,M,L,XL,XXL","Light Blue","Allen Solly","Male",25,1499.0),
    ("P028", "Adidas Essentials T-Shirt","Clothing",  "100% Cotton",      "S,M,L,XL,XXL","White",    "Adidas",   "Male",   60, 1299.0),
    ("P029", "Adidas Essentials T-Shirt","Clothing",  "100% Cotton",      "S,M,L,XL,XXL","Navy",     "Adidas",   "Male",   55, 1299.0),
    ("P030", "Van Heusen Polo T-Shirt", "Clothing",   "Pique Cotton",     "S,M,L,XL",   "Black",    "Van Heusen","Male",  35, 1799.0),
    # Clothing - Women
    ("P031", "Biba Anarkali Kurta",    "Clothing",    "Pure Cotton",      "S,M,L,XL,XXL","Red",      "BIBA",     "Female", 25, 1999.0),
    ("P032", "Biba Anarkali Kurta",    "Clothing",    "Pure Cotton",      "S,M,L,XL,XXL","Blue",     "BIBA",     "Female", 20, 1999.0),
    ("P033", "W Women Kurta Set",      "Clothing",    "Rayon",            "S,M,L,XL",   "Pink",     "W",        "Female", 30, 2499.0),
    ("P034", "Global Desi Dress",      "Clothing",    "Georgette",        "S,M,L,XL",   "Yellow",   "Global Desi","Female",20,2999.0),
    ("P035", "Mango Floral Kurti",     "Clothing",    "Viscose Rayon",    "XS,S,M,L,XL","Multicolor","Mango",   "Female", 15, 2199.0),
    # Footwear
    ("P036", "Nike Air Max 270",       "Footwear",    "Mesh & Rubber",    "6,7,8,9,10,11","White",   "Nike",     "Unisex", 25, 11995.0),
    ("P037", "Nike Air Max 270",       "Footwear",    "Mesh & Rubber",    "6,7,8,9,10,11","Black",   "Nike",     "Unisex", 20, 11995.0),
    ("P038", "Adidas Ultraboost 22",   "Footwear",    "Primeknit & Rubber","6,7,8,9,10,11","Core Black","Adidas", "Unisex",18, 14999.0),
    ("P039", "Puma Softride Enzo",     "Footwear",    "Mesh & EVA",       "6,7,8,9,10",  "Black",    "Puma",     "Male",   30, 3299.0),
    ("P040", "Bata Men's Formal Shoes","Footwear",    "Genuine Leather",  "6,7,8,9,10",  "Black",    "Bata",     "Male",   40, 2499.0),
    ("P041", "Metro Women Heels",      "Footwear",    "Faux Leather",     "4,5,6,7,8",   "Nude",     "Metro",    "Female", 20, 1799.0),
    ("P042", "Bata Women Flats",       "Footwear",    "Leather",          "4,5,6,7,8",   "Brown",    "Bata",     "Female", 35, 1299.0),
]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS products")
    c.execute("""
        CREATE TABLE products (
            product_code   TEXT PRIMARY KEY,
            product_name   TEXT NOT NULL,
            category       TEXT,
            material       TEXT,
            size           TEXT,
            color          TEXT,
            brand          TEXT,
            gender         TEXT,
            stock_quantity INTEGER DEFAULT 0,
            price          REAL
        )
    """)

    c.executemany("""
        INSERT INTO products VALUES (?,?,?,?,?,?,?,?,?,?)
    """, PRODUCTS)

    conn.commit()
    print(f"✅  Database created at: {DB_PATH}")
    print(f"✅  Inserted {len(PRODUCTS)} products")
    
    # Quick verify
    c.execute("SELECT COUNT(*) FROM products")
    count = c.fetchone()[0]
    print(f"✅  Total products in DB: {count}")
    conn.close()

if __name__ == "__main__":
    init_db()
