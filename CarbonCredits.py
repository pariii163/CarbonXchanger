import sqlite3
from prettytable import PrettyTable

# Database Initialization
DB_PATH = "carbon_credits.db"

def create_database():
    """Create the database table if not exists"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            allowed_emissions INTEGER, 
            actual_emissions INTEGER DEFAULT 0,
            credits INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def register_company(name, allowed_emissions):
    """Register a new company with an emission limit"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO companies (name, allowed_emissions, credits) VALUES (?, ?, ?)",
                   (name, allowed_emissions, allowed_emissions))  # Initial credits = allowed emissions
    conn.commit()
    conn.close()
    print(f"✅ Company '{name}' registered successfully!")

def update_emissions(company_name, actual_emissions):
    """Update a company's emissions and adjust credits"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT allowed_emissions FROM companies WHERE name=?", (company_name,))
    result = cursor.fetchone()
    
    if result:
        allowed_emissions = result[0]
        new_credits = allowed_emissions - actual_emissions
        
        cursor.execute("UPDATE companies SET actual_emissions=?, credits=? WHERE name=?", 
                       (actual_emissions, new_credits, company_name))
        conn.commit()
        conn.close()
        print(f"✅ Emissions updated for '{company_name}'. Remaining credits: {new_credits}")
    else:
        print("❌ Company not found!")

def trade_credits(seller, buyer, amount):
    """Allow one company to sell credits to another"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT credits FROM companies WHERE name=?", (seller,))
    seller_credits = cursor.fetchone()
    
    cursor.execute("SELECT credits FROM companies WHERE name=?", (buyer,))
    buyer_credits = cursor.fetchone()
    
    if seller_credits and buyer_credits:
        if seller_credits[0] >= amount:
            new_seller_credits = seller_credits[0] - amount
            new_buyer_credits = buyer_credits[0] + amount
            
            cursor.execute("UPDATE companies SET credits=? WHERE name=?", (new_seller_credits, seller))
            cursor.execute("UPDATE companies SET credits=? WHERE name=?", (new_buyer_credits, buyer))
            conn.commit()
            conn.close()
            print(f"✅ {seller} sold {amount} credits to {buyer}.")
        else:
            print("❌ Seller does not have enough credits!")
    else:
        print("❌ One or both companies not found!")

def display_companies():
    """Show all companies and their carbon credit status"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, allowed_emissions, actual_emissions, credits FROM companies")
    companies = cursor.fetchall()
    conn.close()

    table = PrettyTable(["Company", "Allowed Emissions", "Actual Emissions", "Credits"])
    for company in companies:
        table.add_row(company)
    
    print(table)

# Initialize database
create_database()

# Sample usage
while True:
    print("\n🌍 Carbon Credit Trading System")
    print("1️⃣ Register Company")
    print("2️⃣ Update Emissions")
    print("3️⃣ Trade Credits")
    print("4️⃣ Display Companies")
    print("5️⃣ Exit")

    choice = input("Enter choice: ").strip()
    
    if choice == "1":
        name = input("Enter Company Name: ").strip()
        limit = int(input("Enter Allowed Emissions (in tons): ").strip())
        register_company(name, limit)
    
    elif choice == "2":
        name = input("Enter Company Name: ").strip()
        emissions = int(input("Enter Actual Emissions (in tons): ").strip())
        update_emissions(name, emissions)
    
    elif choice == "3":
        seller = input("Enter Seller Company Name: ").strip()
        buyer = input("Enter Buyer Company Name: ").strip()
        amount = int(input("Enter Credits to Trade: ").strip())
        trade_credits(seller, buyer, amount)
    
    elif choice == "4":
        display_companies()
    
    elif choice == "5":
        print("🚪 Exiting...")
        break
    
    else:
        print("❌ Invalid Choice! Try again.")
