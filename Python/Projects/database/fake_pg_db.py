
import psycopg2
from faker import Faker

fake = Faker()

# this initialize to empty set to keep track of generated email for uniqueness as email is unique
# without this Faker might generate duplicate email 
used_emails = set()

# Connect to database
conn = psycopg2.connect(
        dbname = "test_sh",
        user = "shikhar_insurance_user",
        password = "Al1*+1IJSJA92Fd3",
        host = "localhost"
    
)

# Cursor command to execute SQL commands
cursor = conn.cursor()

# Fetch all IDs and existing usernames from the users_user table
cursor.execute("SELECT id, username FROM users_user")
user_data = cursor.fetchall()
used_usernames = []
# Populate the used_usernames set with existing usernames from the database
for _, username in user_data:
    if username:  # Avoid None or NULL values
        used_usernames.append(username)

# Fetch only user IDs for iteration
user_ids = [row[0] for row in user_data]

# Loop through user IDs and generate fake data
for user_id in user_ids:
    # Ensure unique email
    while True:
        fake_email = fake.email()
        if fake_email not in used_emails:
            used_emails.add(fake_email)
            break

    # Ensure unique username
    while True:
        fake_username = fake.user_name()
        if fake_username not in used_usernames:
            used_usernames.append(fake_username)
            break

    fake_first_name = fake.first_name()
    # Using first_name for middle name since Faker lacks a middle_name method
    fake_middle_name = fake.first_name()
    fake_last_name = fake.last_name()

    # Update the database
    cursor.execute("""
        UPDATE users_user
        SET email = %s, first_name = %s, middle_name = %s, last_name = %s, username = %s
        WHERE id = %s
    """, (fake_email, fake_first_name, fake_middle_name, fake_last_name, fake_username, user_id))

# Commit changes
conn.commit()
cursor.close()
conn.close()

print("Data Duplication complete!! :)")