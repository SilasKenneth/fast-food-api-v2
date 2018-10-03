from app.db import database
database.drop_tables()
database.create_tables()
database.create_default_admin("Silas Kenneth", "silaskenny", "silaskenny@gmail.com", "SilasK@2019")
print("The process has comleted")