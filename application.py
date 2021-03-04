import os
import datetime
from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
app = Flask(__name__)


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def permitinfo(start, end):
    lat=[]
    lon=[]
    dates=[]
    workgroups=[]
    contractors=[]
    communityname=[]
    originaladdress=[]
    x="https://data.calgary.ca/resource/c2es-76ed.geojson?$where=issueddate > "
    y=" and issueddate < "
    z="&$select=issueddate,workclassgroup,contractorname,communityname,originaladdress,latitude,longitude"
    query=x+"'"+start+"'"+y+"'"+end+"'"+z
    result=requests.get(query)
    permits=result.json()
    features=permits.get('features')
    for feature in features:
        permitprop=feature.get('properties')
        lat.append(permitprop.get('latitude'))
        lon.append(permitprop.get('longitude'))
        dates.append(permitprop.get('issueddate'))
        workgroups.append(permitprop.get('workclassgroup'))
        contractors.append(permitprop.get('contractorname'))
        communityname.append(permitprop.get('communityname'))
        originaladdress.append(permitprop.get('originaladdress'))
    return [lat, lon, dates, workgroups, contractors, communityname, originaladdress]

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == 'POST':
        daterange = request.form.get('daterange')
        range=daterange.split()
        st=range[0]
        en=range[2]
        st=st.split('/')
        en=en.split('/')
        start=st[2]+'-'+st[0]+'-'+st[1]
        end=en[2]+'-'+en[0]+'-'+en[1]
        [lat, lon, dates, workgroups, contractors, communityname, originaladdress]=permitinfo(start, end)
        return render_template("main.html", daterange=daterange,lat=lat, lon=lon, dates=dates, workgroups=workgroups, contractors=contractors, communityname=communityname, originaladdress=originaladdress)
    return render_template("main.html")
