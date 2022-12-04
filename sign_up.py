import psycopg2
from dotenv import load_dotenv
from generator import uuid_generator

load_dotenv()

conn = psycopg2.connect('postgres://jwoowfpjmciamf:5e0d687ed33a7de3df899871d1b8c89b3306a6ef37e0e9a72b9b6ec5f44beb20@ec2-34-241-90-235.eu-west-1.compute.amazonaws.com:5432/d7r313ckpbein2',
sslmode= 'require')
class signup():
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.status =True

    def signup_us(self):
        
        sql1 = 'SELECT * FROM users'
        with conn.cursor() as cursor:
            cursor.execute(sql1)
            row= cursor.fetchone()
            while row:
                if str(row[1]) == self.email:
                    self.status=False
                    break
                row= cursor.fetchone()
            
            
            if self.status == True:
                sql2= 'INSERT INTO users (uuid, email, us_password) VALUES (%s, %s, %s)'
                u_uuid = uuid_generator().uid()
                u_email= self.email
                u_password= self.password
                user_data=[u_uuid, u_email, u_password]
                cursor.execute(sql2, user_data)
                conn.commit()

        return self.status
