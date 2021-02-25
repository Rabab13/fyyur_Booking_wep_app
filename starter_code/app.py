# udacity advanced track todo app crud buliding as refrance
# query in sqlalchemy inspire from:
# https://hackersandslackers.com/database-queries-sqlalchemy-orm/

#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from models import Venue, Artist, Show, app, db
import json
import sys
import dateutil.parser
import babel
from sqlalchemy import Integer, String, ForeignKey, Table
from flask import (
Flask,
render_template,
request,
Response,
flash,
redirect,
url_for
)
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from sqlalchemy.sql import func
from flask_wtf import Form
from flask_wtf import FlaskForm
from forms import *
from datetime import date, datetime
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, local= 'en_US')

  app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
@app.route('/venues')
def venues():
  venueareas = db.session.query(func.count(Venue.id), Venue.city, Venue.state)\
    .group_by(Venue.city, Venue.state).all()
  data = []

  for venu in venueareas:
    venue_city_state = Venue.query.filter_by(state = venu.state).filter_by(city = venu.city).all()
    venue_data = []
    for venue in venue_city_state:
      venue_data.append({
        "id": venue.id,
        "name": venue.name, 
        "num_upcoming_shows": len(db.session.query(Show).filter(Show.venue_id==1)\
          .filter(Show.start_time > datetime.today()).all())
      })
    data.append({
      "city": venu.city,
      "state": venu.state, 
      "venues": venue_data
    })

  return render_template('pages/venues.html', areas=data)
  

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  search_venue = db.session.query(Venue).filter(Venue.name.ilike(f'%{search_term}%')).all()
  data = []

  for Svenue in search_venue:
    data.append({
      "id": Svenue.id,
      "name": Svenue.name,
      "num_upcoming_shows": len (db.session.query(Show)\
      .filter(Show.venue_id == Svenue.id)\
      .filter(Show.start_time > datetime.today()).all())
    })
  response={
    "count": len(search_venue),
    "data": data
    }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  global data
  venue = db.session.query(Venue).get(venue_id)

  if not venue:
    flash ('Not found')


  venuepastshows_qy = db.session.query(Show).join(Artist)\
  .filter(Show.venue_id == venue_id)\
  .filter(Show.start_time <= datetime.today()).all()
  past_shows_qy = []

  venueupcomingshows_qy = db.session.query(Show).join(Artist)\
  .filter(Show.venue_id == venue_id)\
  .filter(Show.start_time > datetime.today()).all()
  upcoming_shows_qy = []

  for show in past_shows_qy:
    venuepastshows_qy.append({
      "artist_id": show.artist_id,
      "artist_name":show.artist.name,
      "artist_image_link":show.artist.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%d %H:%S:%M')
    })
  for show in upcoming_shows_qy:
    venueupcomingshows_qy.append({
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%d %H:%S:%M')
    })

  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "image_link": venue.image_link,
    "website": venue.website,
    "facebook_link": venue.website,
    "seeking_venue": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "past_shows":past_shows_qy,
    "upcoming_shows":upcoming_shows_qy,
    "past_shows_count": len(past_shows_qy),
    "upcoming_shows_count": len(upcoming_shows_qy)
  }  
 
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  Venue_form = VenueForm()
  try: 
    vname = Venue_form['name'].data
    vcity = Venue_form['city'].data
    vstate = Venue_form['state'].data
    vaddress = Venue_form['address'].data
    vphone = Venue_form['phone'].data
    vimage_link = Venue_form['image_link'].data
    vgenres = Venue_form['genres'].data
    vgenresarray = []
    vgenresarray = vgenres
    vfacebook_link = Venue_form['facebook_link'].data
    vwebsite = Venue_form['website'].data
    vseeking_talent = Venue_form['seeking_talent'].data
    vseeking_description = Venue_form['seeking_description'].data
    new_venue = Venue()
    new_venue.name = vname
    new_venue.city = vcity
    new_venue.state=vstate
    new_venue.address=vaddress
    new_venue.phone=vphone
    new_venue.genres=vgenres
    new_venue.facebook_link=vfacebook_link
    new_venue.image_link=vimage_link
    new_venue.website=vwebsite
    new_venue.seeking_talent=vseeking_talent
    new_venue.seeking_description=vseeking_description
    db.session.add(new_venue)
    db.session.commit()
    flash('Venue  vname  was successfully listed!')
  except ValueError as e:
    print(e)
    flash('Oops error!')
    db.session.rollback()
  finally:
    db.session.close()

  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  error = False
  try:
    venuedelete = db.session.query(Venue).get(venue_id)
    db.session.delete(venuedelete)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
    
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = db.session.query(Artist).all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  search_artist = db.session.query(Artist).filter(Artist.name.ilike(f'%{search_term}%')).all()
  data = []

  for Sartist in search_artist:
    data.append({
      "id": Sartist.id,
      "name": Sartist.name,
      "num_upcoming_shows": len(db.session.query(Show)\
        .filter(Show.artist_id == Sartist.id)\
          .filter(Show.start_time > datetime.today()).all()),
    })
  
  response={
    "count": len(search_artist),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_artist=request.form.get('search_artist', ''))
  # inspire from:https://github.com/mwinel/Fyyur/blob/master/app.py
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id): 
  artist = db.session.query(Artist).get(artist_id)

  if not artist:
     return render_template('errors/404.html')


  artistpastshows_qy = db.session.query(Show).join(Venue)\
  .filter(Show.artist_id == artist_id)\
  .filter(Show.start_time <= datetime.today()).all()
  past_shows_qy = []

  artistupcomingshows_qy = db.session.query(Show).join(Venue)\
  .filter(Show.artist_id == artist_id)\
  .filter(Show.start_time > datetime.today()).all()
  upcoming_shows_qy = []

  for show in past_shows_qy:
    artistpastshows_qy.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time":show.start_time.strftime('%Y-%m-%d %H:%S:%M')
    })
  for show in upcoming_shows_qy:
    artistupcomingshows_qy.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time":show.start_time.strftime('%Y-%m-%d %H:%S:%M')
    })

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "image_link": artist.image_link,
    "website": artist.website,
    "facebook_link": artist.website,
    "seeking_venue": artist.seeking_venue,
    "seeking_description":artist.seeking_description,
    "past_shows":past_shows_qy,
    "upcoming_shows":upcoming_shows_qy,
    "past_shows_count": len(past_shows_qy),
    "upcoming_shows_count": len(upcoming_shows_qy)
  }


  #  data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.first_or_404(artist_id)
  form = ArtistForm(obj=artist)
  
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  new_error = False
  artist = db.session.query(Artist).get(artist_id)
  try:
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.genres = request.form.getlist('genres')
    artist.image_link = request.form['image_link']
    artist.facebook_link = request.form['facebook_link']
    artist.seeking_venue = True if 'seeking_venue' in request.form else False
    artist.seeking_description = request.form['seeking_description']
    artist.website = request.form['website']
    db.session.commit()
  except:
    new_error = True
    db.session.rollback()
    print(sys.exc_info)
  finally:
    db.session.close()
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.first_or_404(venue_id)

  form = VenueForm(obj=venue)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  new_error = False
  venue = db.session.query(Venue).get(venue_id)
  try:
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.phone = request.form['phone']
    venue.address = request.form['address']
    venue.genres = request.form.getlist('genres')
    venue.image_link = request.form['image_link']
    venue.facebook_link = request.form['facebook_link']
    venue.website = request.form['website']
    venue.seeking_venue = True if 'seeking_venue' in request.form else False
    venue.seeking_description = request.form['seeking_description']
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()


  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  Artist_form = ArtistForm()
  try:
    aname = Artist_form['name'].data
    acity = Artist_form['city'].data
    astate = Artist_form['state'].data
    aphone = Artist_form['phone'].data
    aimage_link = Artist_form['image_link'].data
    agenres = Artist_form['genres'].data
    agenresarray = []
    agenresarray = agenres
    afacebook_link = Artist_form['facebook_link'].data
    awebsite = Artist_form['website'].data
    aseeking_venue = Artist_form['seeking_venue'].data
    aseeking_description = Artist_form['seeking_description'].data

    new_artist = Artist()
    new_artist.name = aname
    new_artist.city = acity
    new_artist.state=astate
    new_artist.phone=aphone
    new_artist.genres=agenres
    new_artist.facebook_link=afacebook_link
    new_artist.image_link=aimage_link
    new_artist.website=awebsite
    new_artist.seeking_talent=aseeking_venue
    new_artist.seeking_description=aseeking_description
    db.session.add(new_artist)
    db.session.commit()
    flash('Artist aname was successfully listed!')
  except ValueError as e:
    print(e)
    flash('Oops error!')
    db.session.rollback()
  finally:
    db.session.close()
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.') 

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  venueartistshows = db.session.query(Show).join(Artist).join(Venue).all()
  
  data = []

  for show in venueartistshows: 
    data.append({
      "venue_id": show.venue_id,
      "venue_name": show.Venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.Artist.name,
      "artist_image_link": show.Artist.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%d %H:%S:%M')
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  Show_form = ShowForm()
  try:
    newartist = Show_form['artist_id'].data
    newvenue = Show_form['venue_id'].data
    startTime = Show_form['start_time'].data
    new_show = Show()
    new_show.artist_id = newartist
    new_show.venue_id = newvenue
    new_show.start_time = startTime
    db.session.add(new_show)
    db.session.commit()
    flash('Show was successfully listed!')
  except ValueError as e:
    print(e)
    flash('Oops error!')
    db.session.rollback()
  finally:
    db.session.close()
   
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''