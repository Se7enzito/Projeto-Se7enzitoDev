import sqlite3 as sql
from ..funcs.systemCripto import encrypt_message, decrypt_message

class GerenData():
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
    
    def listarUsers(self) -> list:
        with self:
            users = self.cursor.execute("SELECT user FROM users").fetchall()
            
            newUsers = []
            
            for userCript in users:
                userUncript = decrypt_message(userCript[0])
                
                newUsers.append(userUncript)
                
            return newUsers
        
    def listarEmails(self) -> list:
        with self:
            emails = self.cursor.execute("SELECT email FROM users").fetchall()
            
            newEmails = []
            
            for emailCript in emails:
                emailUncript = decrypt_message(emailCript[0])
                
                newEmails.append(emailUncript)
                
            return newEmails
    
    def criarUser(self, user: str, email: str, senha: str, permission: int = 0) -> str:
        with self:
            users = self.listarUsers()
            emails = self.listarEmails()
            
            if user in users:
                return "Nome de utilizador já existe."
            elif email in emails:
                return "Email já existe."
            else:
                userCript = encrypt_message(user)
                emailCript = encrypt_message(email)
                senhaCript = encrypt_message(senha)
                
                self.cursor.execute("INSERT INTO users (user, email, password, permission) VALUES (?,?,?,?)", (userCript, emailCript, senhaCript, permission))
                
                return "Utilizador criado com sucesso."
            
    def getUser(self, user: str) -> list:
        with self:
            userCript = encrypt_message(user)
            
            user = self.cursor.execute("SELECT * FROM users WHERE user=?", (userCript,)).fetchone()
            
            if user:
                userUncript = decrypt_message(user[0])
                emailUncript = decrypt_message(user[1])
                senhaUncript = decrypt_message(user[2])
                
                return [userUncript, emailUncript, senhaUncript, user[3]]
            else:
                return []
            
    def confirmLogin(self, email: str, password: str) -> bool:
        with self:
            emailCript = encrypt_message(email)
            
            user = self.cursor.execute("SELECT password FROM users WHERE email=?", (emailCript,)).fetchone()
            
            if user:
                passwordCript = encrypt_message(password)
                
                if passwordCript == user[0]:
                    return True
                else:
                    return False
            else:
                return False

if __name__ == "__main__":
    pass