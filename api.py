import requests

def permitinfo():
    lat=[]
    lon=[]
    result=requests.get("https://data.calgary.ca/resource/c2es-76ed.geojson?$where=issueddate > '2020-01-21' and issueddate < '2020-01-23'&$select=issueddate,workclassgroup,contractorname,communityname,originaladdress,latitude,longitude")
    permits=result.json()
    features=permits.get('features')[0]
    print (features)
    return [None]

if __name__ == "__main__":
    permitinfo()
