import statistics
import random
import requests
# Functions to manipulate SQL info file
import movie_storage_sql as storage

# API request URL
url = "https://www.omdbapi.com/"

# Menu Options menu_text
menu_text = [
    "0. Exit",
    "1. List movies",
    "2. Add movie",
    "3. Delete movie",
    "4. Update movie",
    "5. Stats",
    "6. Random movie",
    "7. Search movie",
    "8. Movies sorted by rating",
    "9. Generate website"
]

def welcome_message():
    header = "********** My Movies Database **********\n"
    return header


def display_menu(menu_options):
    """Display the menu of numeric options."""
    print()
    for option in menu_options:
        print(option)


def get_user_input():
    """Asks the user for a choice from the menu."""
    try:
        selected_action = input("Enter choice (0-9): ")
        return selected_action
    except ValueError:
        print("\nYou probably did not enter a valid option. Enter choice (0-9):")

def list_movies(movies):
    """Retrieve and display all movies from the database in movies.db."""
    movies = storage.list_movies()
    print(f"{len(movies)} movies in total")
    for movie, data in movies.items():
        print(f"{movie} ({data['year']}): {data['rating']}")


def add_movie(movies_old):
    """Asks the user for film name.Checks if the movie already exits and
        if not the user is prompted for the movie name, uses an API
        to get additional data from the web and stores
         it in the database """
    movie_name = input("Write the name of the film to be added: ").strip().lower()
    while not movie_name:
      print("You entered nothing...")
      movie_name = input("Write the name of the film to be added: ").strip().lower()
    try:
      if movie_name in movies_old.keys():
          print("\n++++ A movie with that name already exists!+++\n")
          print("--> Try instead with a different movie name or with option (4) to modify the movie rating")
          print("     ------------------------------------------------------------------------\n")
      else:
          # API request. Checks connection and generates exception if not good
          params = {"apikey": "2e6d1c1a","t": movie_name}
          try:
              response = requests.get(url, params=params, timeout = 5)
              response.raise_for_status()
              if response.status_code == 200:
                  data = response.json()
              else:
                  print("Error:", response.status_code)

              # SQL storage after fetching for movie data from the API
              if data["Response"] == "False":
                  print("Movie not found! Please try again")
              else:
                  storage.add_movie(data["Title"], data["Year"], data["imdbRating"], data["Poster"])
                  print("\n+++ Your movie has been added +++\n")
          except requests.exceptions.RequestException as e:
              print("API request failed:",e)
    except ValueError:
      print("\n**** You have to enter a number!!\n")


def delete_movie(movies):
    """Prompts the user for the name of the film to be deleted.
        When the film is not en the database a message is displayed so
        it can be tried again. If the movie exist, it is deleted from
        movies.db"""
    movie_2_del = input("Write the name of the film to be deleted: ")
    if movie_2_del in movies.keys():
        storage.delete_movie(movie_2_del)
        print("\n+++ Movie deleted +++\n")
    else:
        print("\n +++ ERROR: That movie is not in the database +++\n")


def update_movie(movies):
    """Prompts the user for the name of the film to be updated.
        When the film is not en the database a message is displayed so
        that it can be entered again. If the movie exist, it is updated in
        movies.db"""
    movie = input("Write the name of the film to be updated: ")
    while not movie:
        print("You entered nothing...")
        movie = input("Write the name of the film to be updated: ")
    try:
        if movie in movies.keys():
            n_rating = float(input("Enter the new rating for the film: "))
            storage.update_movie(movie, n_rating)   ####
            print("\n+++ Movie rating modified +++\n")
        else:
            print("\n +++ ERROR: That movie is not in the database +++\n")
    except ValueError:
        print("\n**** You have to enter a number!!\n")


def print_stats(movies2):
    """Calculates basic statistical parameters (avg rating, median,
    max and min rating) and sorts them from top to the worst rated movie"""
    movie_rating_list = []
    for movie, rating_year in movies2.items():
        rating = rating_year["rating"]
        movie_rating_list.append(rating)

    # Sort the ratings and get max, min rating
    sorted_list = sorted(movie_rating_list)
    average = round(sum(sorted_list) / len(sorted_list), 1)
    median_of = round(statistics.median(sorted_list), 1)
    max_rating = sorted_list[-1]
    min_rating = sorted_list[0]

    # Find the movies with the max, min ratings found above
    for movie, rating_year in movies2.items():
        this_movie_rating = rating_year["rating"]
        this_movie = movie
        if max_rating == this_movie_rating:
            best_movie = this_movie
            print(f"The best movie by rating is: {best_movie}: {max_rating}")
        if min_rating == this_movie_rating:
            worst_movie = this_movie
            print(f"The worst movie by rating is: {worst_movie}: {min_rating}")
    print(f"The average film rating is: {average}")
    print(f"The median of film ratings is: {median_of}\n")


def random_movie(movies3):
    """"Generates a random integer to choose a film from the database
        and displays it"""
    random_int = random.randint(0, len(movies3) - 1)
    rand_movie = list(movies3)[random_int]
    rate_of_random_mov = movies3[rand_movie]
    rate_of_random_movie =rate_of_random_mov["rating"]
    print("\nYour random movie: ", end=" ")
    print(rand_movie, rate_of_random_movie, "\n")


def search_movie(movies4):
    """Searches a movie based on a string entered by
        the user. If there is a match, the found movies
        are displayed"""
    text = input("Search string: ").lower()
    movie_list = list(movies4.items())
    print("\n *** Films that match your search criteria ***\n")
    for i in range(len(movies4)):
        if text in movie_list[i][0].lower():
            print(movie_list[i][0], ": ", movie_list[i][1]["rating"], "\n")

    print("++++++ No other films match your criteria +++++\n")


def sort_movies(movies5):
    """Sorts movies by rating from best to worst"""
    list_of_movies = list(movies5.items())
    list_of_movies.sort(key=lambda x: x[1]["rating"], reverse=True)
    print("\n+++Movies from best to worst: ")
    for i in range(len(list_of_movies)):
        print(list_of_movies[i][0], list_of_movies[i][1]["rating"])
    print()


def generate_website(movies):
    """
    Generate a website with the template index_template.html (and style.css)
    where agrid of the database movies will be displayed with its associated
    poster taken from a movies API
    """
    # Read html template
    with open("html/index_template.html","r",encoding="utf-8") as handel:
        template =handel.read()

    # Fetch movies data from database
    movies_dat = storage.list_movies_html()

    # Generate the movie grid in html and
    #   replace placeholder __TEMPLATE_MOVIE_GRID__
    movie_items = []
    for movie, data in movies_dat.items():
        movie_items.append(f"""
                     <li>
                         <div class="movie">
                             <img class="movie-poster" src="{data['poster']}" alt="{movie} poster"/>
                             <div class="movie-title">{movie}</div>
                             <div class="movie-year">{data['year']}</div>
                         </div>
                     </li>""")
    movie_grid = "\n        ".join(movie_items)
    html_text = template.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

    # index.html file/website creation
    with open("html/index.html","w") as h:
        h.write(html_text)
        print("Website successfully generated")


# Function dispatcher to execute desired actions
func_dispatcher = {
    "1": list_movies,
    "2": add_movie,
    "3": delete_movie,
    "4": update_movie,
    "5": print_stats,
    "6": random_movie,
    "7": search_movie,
    "8": sort_movies,
    "9": generate_website
}

def main():
    print(welcome_message())
    movies = storage.list_movies()    ### Gets the movies info from SQL file.
    display_menu(menu_text)
    while True:
        input_index = get_user_input()
        if input_index == "0":
            print("\n++++ Goodbye!\n")
            break
        # Exec action with func_dispatcher directory
        if input_index in func_dispatcher:
            func_dispatcher[input_index](movies)
            movies = storage.list_movies()
            display_menu(menu_text)
        else:
            print("\n+++ ERROR: Invalid option entered +++\n")
            continue

if __name__ == "__main__":
    main()

