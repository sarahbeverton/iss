#!/usr/bin/env python

__author__ = 'Sarah Beverton'

import requests
import time
import turtle


def get_astros():
    # Prints a list of astronauts currently in space,
    # their ship and how many total
    astro = requests.get('http://api.open-notify.org/astros.json')
    astro_data = astro.json()
    people = astro_data['people']
    for person in people:
        print(person['name'], ":", person['craft'])
    print("Total number of astronauts in space:", astro_data['number'])


def get_next_time():
    # Finds next time ISS will pass over Indianapolis
    indy = requests.get('http://api.open-notify.org/' +
                        'iss-pass.json?lat=39.77&lon=-86.12')
    indy_data = indy.json()
    nextpass = indy_data['response'][0]['risetime']
    next_time = time.ctime(nextpass)
    return next_time


def main():
    get_astros()
    next_time = get_next_time()

    # Maps ISS using Turtle
    s = turtle.Screen()
    t = turtle.Turtle()
    # Set up screen
    s.title("ISS Location Tracker")
    s.bgpic('map.gif')
    s.setup(720, 360)
    s.setworldcoordinates(-180, -90, 180, 90)
    # Set up ISS image
    ISS_image = "iss.gif"
    s.addshape(ISS_image)
    t.shape(ISS_image)
    t.penup()
    # Set Indianapolis location
    indy_lat = 39.77
    indy_lon = -86.12
    indy_t = turtle.Turtle()
    indy_t.shape("circle")
    indy_t.shapesize(0.5)
    indy_t.color("yellow")
    indy_t.penup()
    indy_t.goto(indy_lon, indy_lat)
    indy_t.write(next_time)

    def move_ISS():
        # Set ISS location
        curr_loc = requests.get('http://api.open-notify.org/iss-now.json')
        loc_data = curr_loc.json()
        lat = loc_data['iss_position']['latitude']
        lon = loc_data['iss_position']['longitude']
        timestamp = loc_data['timestamp']
        ct = time.ctime(timestamp)
        print("Position of ISS on", ct, ": Lat:", lat, "/ Lon:", lon)
        lat = float(lat)
        lon = float(lon)
        t.goto(lon, lat)
        s.ontimer(move_ISS, 3000)

    move_ISS()
    s.mainloop()


if __name__ == '__main__':
    main()
