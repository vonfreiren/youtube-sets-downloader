
from datetime import datetime

from pymongo import MongoClient

from mongodb import personal_information

client = 'mongodb+srv://{0}:{1}@cluster0.dj76ic2.mongodb.net/?retryWrites=true&w=majority'.format(
    personal_information.user, personal_information.password)

myclient = MongoClient(client)

db = myclient["Music"]
company_db = db["Sets"]

def insert_db(title, artist, image, link):
    company_db.insert_many([{'title': title, 'artist': artist, 'image':image, 'link': link, 'date': datetime.now()}])


