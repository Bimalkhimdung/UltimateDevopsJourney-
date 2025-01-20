import psycopg2
from faker import Faker

# Initialize Faker instance
fake = Faker()

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname="faker",
    user="realhrsoft",
    password="realhrsoft",
    host="localhost",  
    port="5432"
)

cursor = conn.cursor()

# Fetch all IDs from the users_userlegalinfo table
cursor.execute("SELECT id FROM users_userlegalinfo")
user_legalinfo_ids = cursor.fetchall()

# Iterate through each ID and update with fake data
for record in user_legalinfo_ids:
    user_legalinfo_id = record[0]

    # Generate fake data
    fake_pan_number = fake.random_number(digits=16, fix_len=True) 
    fake_cit_number = fake.bothify("??###???#####")  
    fake_pf_number = fake.random_number(digits=16, fix_len=True)  
    fake_citizenship_number = fake.random_number(digits=16, fix_len=True)  # 5-digit fake Citizenship number
    fake_ssfid = fake.random_number(digits=16, fix_len=True)  # 11-digit fake SSF ID

    # Update the database with the generated fake data
    cursor.execute("""
        UPDATE users_userlegalinfo
        SET
            pan_number = %s,
            cit_number = %s,
            pf_number = %s,
            citizenship_number = %s,
            ssfid = %s
        WHERE id = %s
    """, (fake_pan_number, fake_cit_number, fake_pf_number, fake_citizenship_number, fake_ssfid, user_legalinfo_id))

# Commit changes and close connections
conn.commit()
cursor.close()
conn.close()

print("Fake data has been successfully updated!")
