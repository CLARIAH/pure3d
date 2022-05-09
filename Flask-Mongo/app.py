from unicodedata import name
from flask import Flask, render_template,request,redirect,url_for #for flask
from bson import ObjectId
from pymongo import MongoClient
import os

#create and configure app
app = Flask(__name__)
title ="Web Interface for Pure 3D metadata"
heading = "Pure 3D: Web Interface for Annotations"

#set config to connect to Mongo database
client = MongoClient("mongodb://127.0.0.1:27017") #connect to mongo uri
db = client.pure3d_db #database
scenes = db.scene #collection

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index') #redirect to index page

@app.route("/")
def index():    
    #Display the Completed Tasks    
    scene_l = scenes.find({"done":"yes"})    
    a2="active"    
    return render_template('index.html',a2=a2,scenes=scene_l,t=title,h=heading) 

@app.route("/all") 
def all_entries ():
	#Display all
	scene_l = scenes.find()
	a1="active"
	return render_template('index.html',a1=a1,scenes=scene_l,t=title,h=heading)

@app.route("/action", methods=['POST']) 
def action ():
	#Adding an entry
    name=request.values.get("name")
    type=request.values.get("type")
    version=request.values.get("version")
    generator=request.values.get("generator")
    copyright=request.values.get("copyright")
    scenes.insert_one({ "name":name, "type":type, "version":version, "generator":generator, "copyright":copyright}).inserted_id
    return redirect("/all")

@app.route("/remove")
def remove ():
	#Deleting a Task with various references
	key=request.values.get("_id")
	scenes.delete_one({"_id":ObjectId(key)})
	return redirect("/")

@app.route("/update")
def update ():
	id=request.values.get("_id")
	task=scenes.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task,h=heading,t=title)

@app.route("/action3", methods=['POST'])
def action3 ():
	#Updating an entry with various references
	name=request.values.get("name")
	type=request.values.get("type")
	version=request.values.get("version")
	generator=request.values.get("generator")
	copyright=request.values.get("copyright")
	id=request.values.get("_id")
	scenes.update_one({"_id":ObjectId(id)}, {'$set':{ "name":name, "type":type, "version":version, "generator":generator, "copyright":copyright }})
	return redirect("/")

@app.route("/search", methods=['GET'])
def search():
	#Searching an item with various references
	key=request.values.get("key")
	refer=request.values.get("refer")
	if(key=="_id"):
		scene_l = scenes.find({refer:ObjectId(key)})
	else:
		scene_l = scenes.find({refer:key})
	return render_template('searchlist.html',scenes=scene_l,t=title,h=heading)

if __name__ == "__main__":

    app.run()

