from backend.libs.funcs.systemCripto import encrypt_message, decrypt_message
import sqlite3 as sql

class GerenData:
    def __init__(self) -> None:
        self.database = "backend/libs/db/database.db"
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        self.connection = sql.connect(self.database)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
        
    def criarTabelas(self) -> None:
        with self:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS users (user TEXT PRIMARY KEY UNIQUE, email TEXT NOT NULL UNIQUE, password TEXT NOT NULL, permission INTEGER NOT NULL)")

if __name__ == "__main__":
    pass