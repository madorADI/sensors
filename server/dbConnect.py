from flask import Flask, request, json
import psycopg2
import jwt

app = Flask(__name__)

con = psycopg2.connect(
   database="sensordb",
   user="postgres",
   password="password",
   host="10.252.30.196",
   port= '5432'
   )
curs_obj = con.cursor()

def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


@app.route('/image')
def get_images():
   postgreSQL_select_Query = "SELECT * FROM sensors.images;"
   curs_obj.execute(postgreSQL_select_Query)
   return curs_obj.fetchall()

@app.route('/image/<imageID>')
def get_image_by_id(imageID):
   curs_obj.execute("SELECT * FROM sensors.images WHERE image_id = {0};".format(imageID))
   return curs_obj.fetchall()

@app.route('/image/sensor/<sensorID>')
def get_image_by_sensor_id(sensorID):
   curs_obj.execute("SELECT * FROM sensors.images WHERE sensor_id = {0};".format(sensorID))
   return curs_obj.fetchall()

@app.route('/image/<locationX>/<locationY>')
def get_image_by_location(locationX, locationY):
   curs_obj.execute("SELECT * FROM sensors.images WHERE location_x = {0} AND location_y = {1};".format(locationX, locationY))
   return curs_obj.fetchall()

@app.route('/image/post', methods=['POST'])
def post_image():
   data = request.json
   isAlive = data["isAlive"] != 2
   curs_obj.execute(f"INSERT INTO sensors.images(location_x, location_y, sensor_id, path, timestamp, sensor_type, is_alive) VALUES(%s,%s,%s,%s,%s,%s,%s);",(str(data["locationX"]), str(data["locationY"]), str(data["sensorID"]), data["path"], str(data["timeStamp"]), str(data["sensorType"], str(isAlive))))
   con.commit()
   return "1"
if __name__ == '__main__':
   app.run()