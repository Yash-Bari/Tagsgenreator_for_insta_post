import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import mysql.connector

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

db = mysql.connector.connect(
    host="localhost",
    user="",        # Replace with your MySQL username
    password="",        # Replace with your MySQL password
    database="image_db"
)

cursor = db.cursor()

model = tf.keras.applications.ResNet50(weights='imagenet')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def process_image(image_path):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.keras.applications.resnet50.preprocess_input(img_array)
    img_array = tf.expand_dims(img_array, 0)
    predictions = model.predict(img_array)
    decoded_predictions = tf.keras.applications.resnet50.decode_predictions(predictions)[0]

    return decoded_predictions

@app.route('/')
def index():
    search_tags = request.args.get('tags')
    if search_tags:
        cursor.execute("SELECT id, filename, filepath FROM images WHERE id IN (SELECT image_id FROM tags WHERE tag_name LIKE %s)",
                       (f'%{search_tags}%',))
    else:
        cursor.execute("SELECT id, filename, filepath FROM images")
    
    images = cursor.fetchall()
    
    images_data = []

    for image in images:
        cursor.execute("SELECT tag_name, confidence FROM tags WHERE image_id = %s", (image[0],))
        image_tags = cursor.fetchall()

        image_data = {
            'id': image[0],
            'filename': image[1],
            'filepath': image[2],
            'tags': image_tags
        }

        images_data.append(image_data)

    return render_template('index.html', images=images_data)



@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        image = request.files['image']
        if image.filename == '' or not allowed_file(image.filename):
            return redirect(request.url)
        
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            
            # Process the image and extract tags using the process_image function
            tags = process_image(image_path)
            
            # Store image and tag data in the MySQL database
            cursor.execute("INSERT INTO images (filename, filepath) VALUES (%s, %s)", (filename, image_path))
            image_id = cursor.lastrowid
            for tag_info in tags:
                tag_name = tag_info[1]
                confidence = float(tag_info[2])  
                cursor.execute("INSERT INTO tags (image_id, tag_name, confidence) VALUES (%s, %s, %s)",(image_id, tag_name, confidence))
            db.commit()
            
            return redirect(url_for('index'))
    
    return render_template('upload.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_tags = request.form.get('search_tags')
        cursor.execute("SELECT i.id, i.filename, i.filepath, t.tag_name, t.confidence FROM images i "
                       "JOIN tags t ON i.id = t.image_id WHERE t.tag_name LIKE %s", ('%' + search_tags + '%',))
        search_results = cursor.fetchall()
        return render_template('search_results.html', results=search_results)
    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)
