import psycopg2
from faker import Faker
from slugify import slugify
import getpass

fake = Faker()

# Database connection setup
db_name = input("Enter your database name here: ")
db_user = input("Enter your database username here: ")
db_pass = getpass.getpass("Enter your database password here: ")
db_host = input("Enter database host [Enter for default localhost]: ") or "localhost"

def connect_to_db():
    return psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_pass,
        host=db_host,
        port="5432"
    )

# function to fetch data from db
def fetch_all(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()
#function to  update table

def update_table(cursor, query, values):
    cursor.execute(query, values)

#function to generate unique values
def generate_unique_value(existing_set, generator_func):
    while True:
        value = generator_func()
        if value not in existing_set:
            existing_set.add(value)
            return value

# fake username,email,firstname,middlename,lastname
def fake_users_user(conn):
    with conn.cursor() as cursor:
        user_data = fetch_all(cursor, "SELECT id, username FROM users_user")
        used_emails = set()
        used_usernames = {username for _, username in user_data if username}

        for user_id, _ in user_data:
            fake_email = generate_unique_value(used_emails, fake.email)
            fake_username = generate_unique_value(used_usernames, fake.user_name)
            fake_first_name = fake.first_name()
            fake_middle_name = fake.first_name()
            fake_last_name = fake.last_name()

            update_table(
                cursor,
                """
                UPDATE users_user
                SET email = %s, first_name = %s, middle_name = %s, last_name = %s, username = %s
                WHERE id = %s
                """,
                (fake_email, fake_first_name, fake_middle_name, fake_last_name, fake_username, user_id)
            )
        print("Fake data generated for users_user")

#fake userlegal information        

def fake_users_userlegalinfo(conn):
    with conn.cursor() as cursor:
        user_legalinfo_ids = fetch_all(cursor, "SELECT id FROM users_userlegalinfo")
        for (user_legalinfo_id,) in user_legalinfo_ids:
            update_table(
                cursor,
                """
                UPDATE users_userlegalinfo
                SET
                    pan_number = %s,
                    cit_number = %s,
                    pf_number = %s,
                    citizenship_number = %s,
                    ssfid = %s
                WHERE id = %s
                """,
                (
                    fake.random_number(digits=16, fix_len=True),
                    fake.bothify("??###???#####"),
                    fake.random_number(digits=16, fix_len=True),
                    fake.random_number(digits=16, fix_len=True),
                    fake.random_number(digits=16, fix_len=True),
                    user_legalinfo_id
                )
            )
        print("Fake data generated for users_userlegalinfo!")

#fake user contact details
def fake_users_usercontactdetails(conn):
    with conn.cursor() as cursor:
        contact_data = fetch_all(cursor, "SELECT id, slug FROM users_usercontactdetail")

        # Create a set of already used slugs to ensure uniqueness
        used_slugs = {slug for _, slug in contact_data if slug}

        for contact_id, _ in contact_data:
            # Generate a unique slug using the provided `generate_unique_value` function
            fake_slug = generate_unique_value(used_slugs, lambda: slugify(fake.name()))
            fake_number = fake.phone_number()
            fake_contact_of = fake.random_element(elements=("Spouse", "Parent", "Sibling", "Friend"))
            fake_name = fake.name()
            fake_address = fake.address()
            fake_email = fake.email()

            update_table(
                cursor,
                """
                UPDATE users_usercontactdetail
                SET slug = %s, number = %s, contact_of = %s, name = %s, address = %s, email = %s
                WHERE id = %s
                """,
                (fake_slug, fake_number, fake_contact_of, fake_name, fake_address, fake_email, contact_id)
            )

        print("Fake data generated for users_usercontactdetails!")

#fake organization common bank
def fake_common_bank(conn):
    with conn.cursor() as cursor:
        bank_data = fetch_all(cursor, "SELECT id, slug, name FROM common_bank")
        used_slugs = {slug for _, slug, _ in bank_data if slug}
        used_names = {name for _, _, name in bank_data if name}

        for bank_id, _, _ in bank_data:
            fake_name = generate_unique_value(used_names, fake.company)
            fake_slug = generate_unique_value(used_slugs, lambda: slugify(fake_name))
            fake_address = fake.address()
            fake_acronym = "".join(word[0].upper() for word in fake_name.split()[:3])

            update_table(
                cursor,
                """
                UPDATE common_bank
                SET slug = %s, address = %s, name = %s, acronym = %s
                WHERE id = %s
                """,
                (fake_slug, fake_address, fake_name, fake_acronym, bank_id)
            )
        print("Fake data generated for common_bank!")

# ----- fake userbank details
def fake_users_userbank(conn):
    with conn.cursor() as cursor:
        bank_data = fetch_all(cursor, "SELECT id, account_number FROM users_userbank")
        used_account_numbers = {account_number for _, account_number in bank_data if account_number}

        for bank_id, _ in bank_data:
            fake_account_number = generate_unique_value(used_account_numbers, lambda: fake.numerify("###############"))

            update_table(
                cursor,
                "UPDATE users_userbank SET account_number = %s WHERE id = %s",
                (fake_account_number, bank_id)
            )
        print("Fake data generated for users_userbank!")

# --- Delete Data from common_smtpserver ---
def delete_common_smtpserver(conn):
    with conn.cursor() as cursor:
        try: 
           cursor.execute("SELECT COUNT(*) FROM common_smtpserver")
           count = cursor.fetchone()[0]
   
           if count > 0:
               cursor.execute("DELETE FROM common_smtpserver")
               conn.commit()
               print("Data deleted from common_smtpserver!")
           else:
             print("No data found in common_smtpserver.")
        except Exception as e:
           print(f"Error deleting data from common_smtpserver: {e}")

# --- Update superuser details for user login ---
def update_superuser(conn):
    with conn.cursor() as cursor:
        superusers = fetch_all(cursor, "SELECT id FROM users_user WHERE is_superuser = TRUE")
        for (user_id,) in superusers:
            try:
                update_table(
                    cursor,
                    """
                    UPDATE users_user
                    SET username = %s, password = %s
                    WHERE id = %s
                    """,
                    ('realhrsoft', 'pbkdf2_sha256$260000$V8oiIdp0Wk6xKkzDcTyTRC$cvyOom6vxU3kV9RaWP1WRm7Mjg2e9zIepNnJWxsAJJ0=', user_id)
                )
                print(f"Superuser with user_id: {user_id} updated successfully.")
            except psycopg2.Error as e:
                print(f"Failed to update superuser {user_id}: {e}")


# main function call 
if __name__ == "__main__":
    try:
        with connect_to_db() as conn:
            fake_users_user(conn)
            fake_users_userlegalinfo(conn)
            fake_users_usercontactdetails(conn)
            fake_common_bank(conn)
            fake_users_userbank(conn)
            delete_common_smtpserver(conn)
            update_superuser(conn)
            print("All tables have been updated with fake data")
    except psycopg2.Error as e:
        print(f"Database error: {e}")
