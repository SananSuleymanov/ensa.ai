import datetime
import psycopg2
conn = psycopg2.connect('postgres://jwoowfpjmciamf:5e0d687ed33a7de3df899871d1b8c89b3306a6ef37e0e9a72b9b6ec5f44beb20@ec2-34-241-90-235.eu-west-1.compute.amazonaws.com:5432/d7r313ckpbein2',
sslmode= 'require')

class sql:

    def point_id(self, modul):
      with conn.cursor() as cursor:
        sql = 'SELECT point_id FROM points WHERE points_name = (%s)'
        cursor.execute(sql, [str(modul)])
        row = cursor.fetchone()[0]

      return row


    def get(self, point):
        global  point1
        
        point1 = point

        with conn.cursor() as cursor:
                sql = "SELECT * FROM inputs WHERE uuid = (SELECT uuid FROM users WHERE email = (%s)) AND point_id = (SELECT point_id FROM points WHERE points_name = (%s)) ORDER BY input_time DESC LIMIT 1"
                rec = [email1, point1]
                cursor.execute(sql, rec)
                row = cursor.fetchone()

        return str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6])

    def send(self, co2, humidity, pred, val0, val1, val2, uuid, point_name):
    
            with conn.cursor() as cursor:
                sql = "INSERT INTO inputs (co2_value, humidity_value, prediction, value_0, value_1, value_2, uuid, point_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                hum = str(humidity)
                co2 = str(co2)
                uuid = str(uuid)
                point1_id = self.point_id(point_name)
                record = [co2, hum, pred, val0, val1, val2, uuid, point1_id]
                cursor.execute(sql, record)
                conn.commit()

    def array(self):
       
        with conn.cursor() as cursor:
                sql = "SELECT * FROM inputs WHERE input_time > now() - interval ' 1 hour' AND uuid = (SELECT uuid FROM users WHERE email = (%s)) AND point_id = (SELECT point_id FROM points WHERE points_name = (%s)) ORDER BY input_time"
                rec = [email1, point1]
                cursor.execute(sql, rec)
                row = cursor.fetchone()
                array1 = [] #time
                array2 = [] #co2
                array3 = [] #humidity
                while row:
                    time = datetime.datetime.strptime(str(row[0]), '%Y-%m-%d %H:%M:%S.%f%z')
                    array1.append(time.strftime('%H:%M:%S'))
                    array2.append(int(row[1]))
                    array3.append(int(row[2]))
                    row = cursor.fetchone()

        return array1, array2, array3
    
    def points_get(self, email):
        global email1
        email1 = email
        with conn.cursor() as cursor:
            sql = 'SELECT points_name FROM points WHERE uuid = (SELECT uuid FROM users WHERE email = (%s))'
            email = [email1]
            cursor.execute(sql, email)
            row = cursor.fetchone()
            points = []
            while row:
                points.append(str(row[0]))
                row = cursor.fetchone()
        
        return points

            
