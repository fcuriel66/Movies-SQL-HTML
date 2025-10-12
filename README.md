# Movies-SQL-HTML

A small project that builds a static website of movies, feeding content from an SQL database (populated via a movies API), and renders the data in HTML + CSS.

---

## 🚀 Features

- Uses **SQLite** as the storage backend to persist movie data.  
- Populates the database from a remote **movies API**.  
- Generates a styled HTML page (with CSS) that lists movies along with title, year, poster image, etc.  
- Simple static output—easy to host or view locally without a server.

---

## 📁 Project Structure
```
Movies-SQL-HTML/
├── data/
│ └── movies.db # SQLite database file
├── html/
│ ├── index.html # HTML of website
│ ├── index_template.html # HTML template to populate with movies grid
│ └── style.css # CSS stylesheet
├── movies.py # Script (or module) for interacting with the movies API
├── movie_storage_sql.py # Module for database storage/query logic
└── README.md
```
---

## 🛠️ Setup & Usage

1. **Clone the repository**

   git clone https://github.com/fcuriel66/Movies-SQL-HTML.git
   cd Movies-SQL-HTML

2. **Run the Python code**

python movies.py

3. **View the website**

open html/index.html   # macOS
# or
xdg-open html/index.html   # Linux

