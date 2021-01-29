from flask import Flask, request, send_file
from flask_mysqldb import MySQL
import os
import base64
import cloudinary as Cloud
from PIL import Image

app = Flask(__name__)

def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)
# Cloudinary Connection
# Cloud.config.update = ({
#     'cloud_name':os.environ.get('dt7arlzmh'),
#     'api_key': os.environ.get('237526652339456'),
#     'api_secret': os.environ.get('sFMd0D7wI2cJgvQXUsyrMnGtOHk')
# })

# desert = Cloud.CloudinaryImage("Desert.jpg")
# print(type(desert))
# print(desert.url)
# MySql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sports_synthesis'

mysql = MySQL(app)

@app.route('/storeimage',methods=['POST'])
def store_image():
  
    image_url = "C:\\Users\\Public\\Pictures\\Sample Pictures\\Hydrangeas.jpg"
    image = convertToBinaryData(image_url)
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO image(image_blob) VALUES (%s)",[image])
    mysql.connection.commit()
    cur.close()
    return 'Image Stored Sucessfully'

@app.route('/getimage',methods=['GET'])
def get_image():
    id = request.args['id']
    cur = mysql.connection.cursor()
    cur.execute("""SELECT image_blob FROM image WHERE image_id = %s""",(id,))
    data = cur.fetchone()
    img_blob = data[0]
    # img = base64.decodebytes(data)
    # print(img)
    print(type(img_blob))
    img_str = base64.decodebytes(img_blob)
    print(type(img_str))
    
    return img_str
    
    
    


if __name__ == '__main__':
    app.run()