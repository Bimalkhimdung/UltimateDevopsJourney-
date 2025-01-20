import psycopg2
from faker import Faker

fake = Faker()

# Initialize empty sets to keep track of generated unique values
used_account_numbers = set()

# Connect to the database
conn = psycopg2.connect(
    dbname="faker",
    user="realhrsoft",
    password="realhrsoft",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# --- Fake users_userbank table ---
# Fetch all IDs and existing account numbers from the users_userbank table
cursor.execute("SELECT id, account_number FROM users_userbank")
bank_data = cursor.fetchall()

# Populate the used_account_numbers set with existing account numbers
for _, account_number in bank_data:
    if account_number:  # Avoid None or NULL values
        used_account_numbers.add(account_number)

# Fetch only bank IDs for iteration
bank_ids = [row[0] for row in bank_data]

# Loop through bank IDs and generate fake account numbers
for bank_id in bank_ids:
    # Ensure unique account number
    while True:
        fake_account_number = fake.numerify("###############")  # Generate a 14-digit account number
        if fake_account_number not in used_account_numbers:
            used_account_numbers.add(fake_account_number)
            break

    # Update the database
    cursor.execute("""
        UPDATE users_userbank
        SET account_number = %s
        WHERE id = %s
    """, (fake_account_number, bank_id))

# Commit changes
conn.commit()
cursor.close()
conn.close()

print("Data Duplication complete!! :)")
