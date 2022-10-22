import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect('postgres://jwoowfpjmciamf:5e0d687ed33a7de3df899871d1b8c89b3306a6ef37e0e9a72b9b6ec5f44beb20@ec2-34-241-90-235.eu-west-1.compute.amazonaws.com:5432/d7r313ckpbein2',
sslmode= 'require')
class signin():
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.status =None

    def login_us(self):
        
        sql = 'SELECT * FROM users'
        with conn.cursor() as cursor:
            cursor.execute(sql)
            row= cursor.fetchone()
            while row:
                
                 if str(row[1]) == self.email and str(row[2]) == self.password:
                     self.status = True
                     break
                 else:
                     self.status = False
                 row= cursor.fetchone()

        return self.status

