import requests
from models import db
from models import Book
from secret import API_KEY



response= requests.get(f"https://www.googleapis.com/books/v1/volumes?q=search-terms&key={API_KEY} &maxResults=40")
data = response.json()
res = response.json()
data = res["items"]


for volume in data:
    title = volume["volumeInfo"]["title"]
    #description = volume["volumeInfo"]["description"]
    
    if "volumeInfo" in volume and "description" in volume["volumeInfo"]:
      description = volume["volumeInfo"]["description"]
else:
    
    description = "Description not available"
    
if "authors" in volume.get("volumeInfo", {}):
    authors = volume["volumeInfo"]["authors"]
else:
    # Handle the case where 'authors' is not present
    authors = []  # Or another default value


    book = Book(name= title, author= authors, description=description)
    db.session.add(book)
    db.session.commit()
    
    

     
    


         
