
import psycopg2
from faker import Faker
from slugify import slugify
import getpass

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

if __name__ == "__main__":
    super_user()