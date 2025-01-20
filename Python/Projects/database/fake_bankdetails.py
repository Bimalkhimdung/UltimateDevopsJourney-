import psycopg2
from faker import Faker
from slugify import slugify  

fake = Faker()

# Initialize empty sets to keep track of unique values
used_slugs = set()
used_names = set()

# Connect to the database
conn = psycopg2.connect(
    dbname="faker",
    user="realhrsoft",
    password="realhrsoft",
    host="localhost"
)

# Cursor command to execute SQL commands
cursor = conn.cursor()

# --- Fake common_bank table ---
# Fetch all IDs and existing slugs and names from the common_bank table
cursor.execute("SELECT id, slug, name FROM common_bank")
bank_data = cursor.fetchall()

# Populate the used_slugs and used_names sets with existing values
for _, slug, name in bank_data:
    if slug:  # Avoid None or NULL values
        used_slugs.add(slug)
    if name:
        used_names.add(name)

# Fetch only bank IDs for iteration
bank_ids = [row[0] for row in bank_data]

# Loop through bank IDs and generate fake data
for bank_id in bank_ids:
    # Ensure unique slug
    while True:
        fake_name = fake.company()  # Generate a fake bank name
        fake_slug = slugify(fake_name)  # Use slugify directly
        if fake_slug not in used_slugs:
            used_slugs.add(fake_slug)
            break

    # Ensure unique bank name
    while True:
        if fake_name not in used_names:
            used_names.add(fake_name)
            break

    # Generate fake address
    fake_address = fake.address()

    # Generate fake acronym (e.g., first letters of the bank name)
    fake_acronym = "".join([word[0].upper() for word in fake_name.split()[:3]])

    # Update the database
    cursor.execute("""
        UPDATE common_bank
        SET slug = %s, address = %s, name = %s, acronym = %s
        WHERE id = %s
    """, (fake_slug, fake_address, fake_name, fake_acronym, bank_id))

# Commit changes
conn.commit()
cursor.close()
conn.close()

print("Data Duplication complete!! :)")
