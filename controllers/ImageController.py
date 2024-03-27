from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from CarApi import db,app 

#TO DO - add a route to upload car photos
#TO DO - add a route to upload user  photos

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/CarPhoto/upload', methods=['POST'])
def upload_car_photo():
    target = os.path.join(APP_ROOT, '..\\images\\cars\\')
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist('file'):
        filename = secure_filename(file.filename)
        destination = '/'.join([target, filename])
        file.save(destination)
    return 'File uploaded successfully', 200  

@app.route('/UserPhoto/upload', methods=['POST'])
def upload_user_photo():
    target = os.path.join(APP_ROOT, '..\\images\\users\\')
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist('file'):
        filename = secure_filename(file.filename)
        destination = '/'.join([target, filename])
        file.save(destination)
    return 'File uploaded successfully', 200  

@app.route('/CarPhoto/<filename>', methods=['DELETE'])
def delete_car_photo():
    target = os.path.join(APP_ROOT, '..\\images\\cars\\')
    if not os.path.isdir(target):
        return "Photo not found", 204
    else:
        filename = request.view_args['filename']
        os.remove(target + filename)
        return "Photo deleted", 200
