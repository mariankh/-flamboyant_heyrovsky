from flask import Flask
from redis import Redis, RedisError
import os
import socket

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons

app = Flask(__name__, template_folder="templates")

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyBGir7uuIvdEOH24VRmNcDCUCHSwmWS6No"

# you can also pass key here
GoogleMaps(app, key="AIzaSyBGir7uuIvdEOH24VRmNcDCUCHSwmWS6No")


@app.route("/")
def mapview():
    lat1=37.4419,
    lng1=-122.1419,
    lat2=37.4300,
    lng2=-122.1400,
    trdmap = Map(
        identifier="trdmap",
        varname="trdmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
            {
                'icon': '/static/green.png',
                'lat': lat1,
                'lng': lng1,
                'infobox': "<b style='color:green;'>GREEN</b>!"
            },
            {
                'icon': '/static/blue.png',
                'lat': lat2,
                'lng': lng2,
                'infobox': "<b style='color:blue;'>BLUE</b>!"
            },
            {
                'icon': '/static/yellow.png',
                'lat': 37.4500,
                'lng': -122.1350,
                'infobox': (
                    "Hello I am <b style='color:#ffcc00;'>YELLOW</b>!"
                    "<h2>It is HTML title</h2>"
                    "<img src='//placehold.it/50'>"
                    "<br>Images allowed!"
                )
            }
        ]
    )
    
    return render_template(
        'example.html',
        trdmap=trdmap
    )


@app.route('/fullmap')
def fullmap():
    fullmap = Map(
        identifier="fullmap",
        varname="fullmap",
        style=(
            "height:100%;"
            "width:100%;"
            "top:0;"
            "left:0;"
            "position:absolute;"
            "z-index:200;"
        ),
        lat=37.4419,
        lng=-122.1419,
        markers=[
            {
                'icon': '//maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat': 37.4419,
                'lng': -122.1419,
                'infobox': "Hello I am <b style='color:green;'>GREEN</b>!"
            },
            {
                'icon': '//maps.google.com/mapfiles/ms/icons/blue-dot.png',
                'lat': 37.4300,
                'lng': -122.1400,
                'infobox': "Hello I am <b style='color:blue;'>BLUE</b>!"
            },
            {
                'icon': icons.dots.yellow,
                'title': 'Click Here',
                'lat': 37.4500,
                'lng': -122.1350,
                'infobox': (
                    "Hello I am <b style='color:#ffcc00;'>YELLOW</b>!"
                    "<h2>It is HTML title</h2>"
                    "<img src='//placehold.it/50'>"
                    "<br>Images allowed!"
                )
            }
        ],
        # maptype = "TERRAIN",
        # zoom="5"
    )
    return render_template('example_fullmap.html', fullmap=fullmap)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

