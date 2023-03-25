import sqlite3

profiles_db = sqlite3.connect("databases/profiles.db")
profiles = profiles_db.cursor()

profiles.execute("""
    CREATE TABLE IF NOT EXISTS main(
        user_id BIGINT,
        showed_profile_id BIGINT
    )
""")