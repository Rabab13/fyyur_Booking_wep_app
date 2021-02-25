from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
import datetime

app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models.
#----------------------------------------------------------------------------#
# REFRANCE TO CONVERT LIST TO STRING https://www.geeksforgeeks.org/python-program-to-convert-a-list-to-string/
class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.ARRAY(db.String()))
    website = db.Column(db.String(120),nullable=True)
    shows = db.relationship('Show', backref='Venue', lazy=True)
    # lazy dynamic is special and useful if we have many items.
    # Instead of loading the items SQLAlchemy will return another query object which we can further refine before loading the items. 
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))

def __repr__(self):
  return f'Venue {self.name} {self.city} {self.state}>'



class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120),nullable=True)
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    website = db.Column(db.String(120),nullable=True)
    shows = db.relationship('Show', backref='Artist', lazy=True)
    # lazy dynamic is special and useful if we have many items.
    # Instead of loading the items SQLAlchemy will return another query object which we can further refine before loading the items. 
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500), default='')
    
def __repr__(self):
  return f'<Artist {self.name} {self.city} {self.state}>'


class Show(db.Model):
  __tablename__='Show'
  id = db.Column(db.Integer,primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable = False)
  artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"), nullable = False)
  start_time = db.Column(db.DateTime, nullable=False)
  
  
def __repr__(self):
  return f'Show artist_id: {self.artist_id} venue_id: {self.venue_id}' 


  
   
