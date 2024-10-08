import sqlite3 as sql
from ..funcs.systemCripto import encrypt_message, decrypt_message

class GerenData():
    def __init__(self) -> None:
        self.database = "backend/libs/db/database.db"
        self.connection = None
        self.cursor = None
    
    def conectar(self) -> None:
        self.connection = sql.connect(self.database)
        self.cursor = self.connection.cursor()

    def desconectar(self) -> None:
        self.connection.close()
        
    def criarTabelas(self) -> None:
        self.conectar()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            user TEXT PRIMARY KEY UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            permission INTEGER NOT NULL
            );""")
            
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL
            );""")
            
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS notificacoes (
            user TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            sender TEXT NOT NULL,
            visualizado INTEGER NOT NULL
            );""")
            
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS aulas (
            user TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            data TEXT NOT NULL,
            horario TEXT NOT NULL,
            tipo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            ocorreu INTEGER NOT NULL
            );""")
            
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS propostas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            proponente TEXT NOT NULL,
            data TEXT NOT NULL,
            resposta TEXT,
            visualizado INTEGER
            );""")
        
        self.connection.commit()
        self.desconectar()
    
    # Users
    def listarUsers(self) -> list:
        self.conectar()
        users = self.cursor.execute("SELECT user FROM users").fetchall()
        
        newUsers = []
        
        for userCript in users:
            userUncript = decrypt_message(userCript[0])
            
            newUsers.append(userUncript)
            
        self.desconectar()
            
        return newUsers
        
    def listarEmails(self) -> list:
        self.conectar()
        emails = self.cursor.execute("SELECT email FROM users").fetchall()
        
        newEmails = []
        
        for emailCript in emails:
            emailUncript = decrypt_message(emailCript[0])
            
            newEmails.append(emailUncript)
            
        self.desconectar()
            
        return newEmails
    
    def criarUser(self, user: str, email: str, senha: str, permission: int = 0) -> str:
        users = self.listarUsers()
        emails = self.listarEmails()
        self.conectar()
        
        if user in users:
            return "Nome de utilizador já existe."
        elif email in emails:
            return "Email já existe."
        else:
            userCript = encrypt_message(user)
            emailCript = encrypt_message(email)
            senhaCript = encrypt_message(senha)
            
            self.cursor.execute("INSERT INTO users (user, email, password, permission) VALUES (?,?,?,?)", (userCript, emailCript, senhaCript, permission))
            
            self.connection.commit()
            self.desconectar()
            
            return "Utilizador criado com sucesso."
    
    def getUser(self, email: str) -> str:
        self.conectar()
        emailCript = encrypt_message(email)
        
        user = self.cursor.execute("SELECT * FROM users WHERE email=?", (emailCript,)).fetchone()
        
        self.desconectar()
        
        if user:
            userUncript = decrypt_message(user[0])
            
            return userUncript
        else:
            return []
    
    def getUserInfos(self, email: str) -> list:
        self.conectar()
        emailCript = encrypt_message(email)
        
        user = self.cursor.execute("SELECT * FROM users WHERE email=?", (emailCript,)).fetchone()
        
        self.desconectar()
        
        if user:
            userUncript = decrypt_message(user[0])
            emailUncript = decrypt_message(user[1])
            senhaUncript = decrypt_message(user[2])
            
            return [userUncript, emailUncript, senhaUncript, user[3]]
        else:
            return []
            
    def confirmLogin(self, email: str, password: str) -> bool:
        self.conectar()
        emailCript = encrypt_message(email)
        
        user = self.cursor.execute("SELECT password FROM users WHERE email=?", (emailCript,)).fetchone()
        
        self.desconectar()
        
        if user:
            passwordCript = encrypt_message(password)
            
            if passwordCript == user[0]:
                return True
            else:
                return False
        else:
            return False
            
    # Serviços
    def getServicos(self) -> list:
        pass
    
    def getServicoId(self, id: int) -> list:
        pass
    
    # Notificações
    def getNotificacoes(self, user: str) -> list:
        pass
    
    # Aulas
    def getAulas(self, user: str) -> list:
        pass
    
    # Propostas
    def getPropostas(self, user: str) -> list:
        pass
    
    def getRespostas(self, user: str) -> list:
        pass

if __name__ == "__main__":
    pass