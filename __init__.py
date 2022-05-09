from turtle import title
from flask import Flask, render_template,request,redirect,url_for #for flask
from bson import ObjectId
from pymongo import MongoClient
import os

def create_app():
#create and configure app
    app = Flask(__name__)
    title ="Web Interface for Pure 3D metadata"
    heading = "Pure 3D: Web Interface for Annotations"

    #set config to connect to Mongo database
    client = MongoClient("mongodb://127.0.0.1:27017") #connect to mongo uri
    db = client.pure3ddb #database
    datas = db.data #collection
  

    @app.route('/enter_data', methods = ['GET'])
    def enter():
        #enter data
        post_collection=db.posts #create collection
        posts = post_collection.insert_one({'type': 'application/si-dpo-3d.document+json',
                'version': '1.0',
                'generator': 'Some generator',
                'copyright': '(c) Some institute.',
                'scene': '0',
                'scenes': [{'units': 'mm','name': 'Scene','nodes': '0'}],
                'nodes': [{'name': 'building','model': '0'}],
                'models': [{'units': 'm','derivatives': [{'usage': 'Web3D','quality': 'Medium','assets': [{'uri': 'clanwilliam.glb','type': 'Model'}]}]}]
        })
        return render_template('data.html', posts=posts)

    @app.route('/show_all', methods = ['GET'])

    def entry_all():
        scene_collection=db.scenes #create collection
        scenes = scene_collection.find({})
        return render_template('data.html', scenes=scenes)

    return app
