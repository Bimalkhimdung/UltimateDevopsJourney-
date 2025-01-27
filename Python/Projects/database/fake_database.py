import psycopg2
from faker import Faker
from slugify import slugify
import getpass

fake = Faker()
db_name = input("Enter your database name here: ")
db_user = input("Enter your database username here: ")
db_pass = getpass.getpass("Enter your database password here: ")
db_host = input("Enter database host  [ Enter for default localhost ]: ")
if not db_host:
    db_host = "localhost"
# --- Database Connection ---
def connect_to_db():
    return psycopg2.connect(
        dbname = db_name,
        user = db_user,
        password = db_pass,
        host=db_host,
        port="5432"
    )

# --- Fake users_user Table ---
def fake_users_user():
    conn = connect_to_db()
    cursor = conn.cursor()

    # Fetch all IDs and existing usernames
    cursor.execute("SELECT id, username FROM users_user")
    user_data = cursor.fetchall()

    used_emails = set()
    used_usernames = [username for _, username in user_data if username]

    user_ids = [row[0] for row in user_data]

    for user_id in user_ids:
        while True:
            fake_email = fake.email()
            if fake_email not in used_emails:
                used_emails.add(fake_email)
                break

        while True:
            fake_username = fake.user_name()
            if fake_username not in used_usernames:
                used_usernames.append(fake_username)
                break

        fake_first_name = fake.first_name()
        fake_middle_name = fake.first_name()
        fake_last_name = fake.last_name()

        cursor.execute(
            """
            UPDATE users_user
            SET email = %s, first_name = %s, middle_name = %s, last_name = %s, username = %s
            WHERE id = %s
            """,
            (fake_email, fake_first_name, fake_middle_name, fake_last_name, fake_username, user_id)
        )

    conn.commit()
    cursor.close()
    conn.close()
    print("Fake data generated for users_user!")

# --- Fake users_userlegalinfo Table ---
def fake_users_userlegalinfo():
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users_userlegalinfo")
    user_legalinfo_ids = cursor.fetchall()

    for record in user_legalinfo_ids:
        user_legalinfo_id = record[0]
        fake_pan_number = fake.random_number(digits=16, fix_len=True)
        fake_cit_number = fake.bothify("??###???#####")
        fake_pf_number = fake.random_number(digits=16, fix_len=True)
        fake_citizenship_number = fake.random_number(digits=16, fix_len=True)
        fake_ssfid = fake.random_number(digits=16, fix_len=True)

        cursor.execute(
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
            (fake_pan_number, fake_cit_number, fake_pf_number, fake_citizenship_number, fake_ssfid, user_legalinfo_id)
        )

    conn.commit()
    cursor.close()
    conn.close()
    print("Fake data generated for users_userlegalinfo!")

# --- Fake common_bank Table ---
def fake_common_bank():
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, slug, name FROM common_bank")
    bank_data = cursor.fetchall()

    used_slugs = {slug for _, slug, _ in bank_data if slug}
    used_names = {name for _, _, name in bank_data if name}

    bank_ids = [row[0] for row in bank_data]

    for bank_id in bank_ids:
        while True:
            fake_name = fake.company()
            fake_slug = slugify(fake_name)
            if fake_slug not in used_slugs:
                used_slugs.add(fake_slug)
                break

        while True:
            if fake_name not in used_names:
                used_names.add(fake_name)
                break

        fake_address = fake.address()
        fake_acronym = "".join([word[0].upper() for word in fake_name.split()[:3]])

        cursor.execute(
            """
            UPDATE common_bank
            SET slug = %s, address = %s, name = %s, acronym = %s
            WHERE id = %s
            """,
            (fake_slug, fake_address, fake_name, fake_acronym, bank_id)
        )

    conn.commit()
    cursor.close()
    conn.close()
    print("Fake data generated for common_bank!")

# --- Fake users_userbank Table ---
def fake_users_userbank():
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, account_number FROM users_userbank")
    bank_data = cursor.fetchall()

    used_account_numbers = {account_number for _, account_number in bank_data if account_number}

    bank_ids = [row[0] for row in bank_data]

    for bank_id in bank_ids:
        while True:
            fake_account_number = fake.numerify("###############")
            if fake_account_number not in used_account_numbers:
                used_account_numbers.add(fake_account_number)
                break

        cursor.execute(
            """
            UPDATE users_userbank
            SET account_number = %s
            WHERE id = %s
            """,
            (fake_account_number, bank_id)
        )

    conn.commit()
    cursor.close()
    conn.close()
    print("Fake data generated for users_userbank!")

def super_user():
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id  FROM users_user WHERE is_superuser = TRUE")
        superusers = cursor.fetchall()
        for user_id_tuple in superusers:
            user_id = user_id_tuple[0]
            try:
                update_query = """
                    UPDATE users_user
                    SET username = %s, password = %s
                    WHERE id = %s
                """
                hashed_password = 'pbkdf2_sha256$260000$V8oiIdp0Wk6xKkzDcTyTRC$cvyOom6vxU3kV9RaWP1WRm7Mjg2e9zIepNnJWxsAJJ0=' 
                cursor.execute(update_query, ('realhrsoft', hashed_password, user_id))
                conn.commit()
                print("Superuser Updated")
            except (Exception, psycopg2.Error) as update_error:
                conn.rollback()
                print(f"updating username and password is failed: { update_error }")
    except (Exception, psycopg2.Error) as select_error:
            print(f"Got error : { select_error}")
    finally:
        if conn:
            cursor.close()
            conn.close()



# --- Main Function ---
if __name__ == "__main__":
    fake_users_user()
    fake_users_userlegalinfo()
    fake_common_bank()
    fake_users_userbank()
    super_user()
    print("All tables have been updated with fake data!")
