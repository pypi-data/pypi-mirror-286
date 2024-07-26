"""Functionality related to installation of the python package"""

import sqlite3
import warnings
from pathlib import Path


class PersistentDataWarning(Warning):
    pass


def create_package_database_if_not_exists():
    """Creates the local database package_data.sqlite, if it doesn't already exist"""
    package_data_dir = Path.home() / ".happy-rag-friends"
    db_name: str = "package_data.sqlite"
    if not package_data_dir.exists():
        package_data_dir.mkdir(parents=True)

    db_path = package_data_dir / db_name

    if not db_path.exists():
        warnings.warn(
            f"\nPackage data written to {package_data_dir} is not deleted on 'pip uninstall happy-rag-friends' - you will need to delete this folder and it's contents manually",
            PersistentDataWarning,
        )
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.executescript(
            """
    CREATE TABLE IF NOT EXISTS advisors (
        advisor_id INTEGER PRIMARY KEY,
        advisor_name TEXT NOT NULL,
        personality_description TEXT,
        path_to_model TEXT
    )
    ;
    
    INSERT INTO advisors (advisor_id, advisor_name, personality_description, path_to_model)
    VALUES (0, 'D. Folt', 'a knowledgeable advisor.', NULL)
    ;
    """
        )
        conn.commit()
        conn.close()
        print(f"created package database at {db_path}")
