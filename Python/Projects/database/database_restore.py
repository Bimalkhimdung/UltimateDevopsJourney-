import psycopg2

db_connection = psycopg2.connect(
        dbname = "shikhar",
        user = "shikhar_insurance_user",
        password = "Al1*+1IJSJA92Fd3",
        host = "localhost"
)



cursor = db_connection.cursor()

# for commands like CREATE DATABASE, DROP DATABASE this should be executed immediately for 
# autocommit function is used for this 

db_connection.autocommit = True

while True:
    # create object to connect to db
        db_name = input("Enter database name\n")
        db_user = input("Enter database user\n")

        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}';")
        db_exists = cursor.fetchone()

        cursor.execute(f"SELECT 1 FROM pg_roles WHERE rolname = '{db_user}';")
        user_exists = cursor.fetchone()


        if not user_exists:
                user_choice = input(f"Database User {db_user} Dose not exists. Do you want to Create one ? (Y/N): \n").strip().lower()
                if user_choice == "y":
                        user_password = input(f"Enter password for {db_user}: \n")
                        cursor.execute(f"CREATE ROLE {db_user} WITH PASSWORD '{user_password}';")
                        cursor.execute(f"ALTER ROLE {db_user} LOGIN;")
                        print(f"User created Successfully !!")
                else:
                        print("Existing without creating Database and user")
                        break

        if db_exists:
          choice = input(f"{db_name} Database already exists. Do You want to create another one ? (Y/N): \n").strip().lower()
          if choice == "n":
                  print("Exiting without creating database")
                  break
          else:
                  continue



        #else:
        cursor.execute(f"CREATE DATABASE {db_name};")
        cursor.execute(f"GRANT ALL ON DATABASE {db_name} TO {db_user};")
        cursor.execute(f"ALTER DATABASE {db_name} OWNER TO {db_user};")
        
        print(f"Database {db_name} created successfully and ownership granted to user {db_user}.")
        break
        

cursor.close()
db_connection.close()
