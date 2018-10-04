from app.db import database
database.create_tables()
database.create_default_admin("Silas Kenneth", "silaskenny", "silaskenny@gmail.com", "SilasK@2019")