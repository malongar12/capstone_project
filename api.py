import requests
from models import db
from models import Book
from secret import API_KEY
from app import app 


response= requests.get(f"https://www.googleapis.com/books/v1/volumes?q=search-terms&key={API_KEY} &maxResults=40")

if response.status_code == 200:
    res = response.json()
    data = res["items"] or []
    print(data)

    with app.app_context():
        for volume in data:
                title = volume["volumeInfo"].get("title", "No title available")
                description = volume["volumeInfo"].get("description", "Description not available")
                authors = volume["volumeInfo"].get("authors", [])
                
                for author in authors:
                    book = Book(name=title, author=author, description=description)
                db.session.add(book)
                db.session.commit()

else:
    print(f"bad request with a status code of {response.status_code}")




         
