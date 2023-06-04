# Better Foods

[![Video Demo](https://www.youtube.com/watch?v=HA6ljpb-dPA)](https://www.youtube.com/watch?v=HA6ljpb-dPA)

## Description

Better Foods is a sophisticated website that leverages the power of Google Maps and Yelp APIs to provide users with an exceptional dining experience. The website allows users to explore and discover highly-rated restaurants in their desired locality, while also enabling them to create a personalized database of their visited and reviewed restaurants.

## Features

- **Search**: The Search page is the lifeline of the website, where users can interact and find restaurants. Users can input a specific location, and the website makes parallel API calls to Google Maps and Yelp to retrieve relevant restaurant data. The search query is reverse-geocoded to obtain the coordinates of the location, which are then used to fetch nearby restaurants from both the Google Places API and the Yelp API.

- **Filtering**: The retrieved restaurant data is filtered based on various parameters, including operational status, address, name, average rating, price level, and distance from the search query. The Haversine method is employed to calculate the distance between the search query and each restaurant, ensuring accurate results.

- **Details**: The Details page provides users with further information about a specific restaurant, including top reviews and the restaurant's website. Users can dive deeper into their restaurant exploration journey.

- **Visit**: When users decide to visit a particular restaurant, the entry is stored in the database for later review. The Visit page allows users to keep track of their visited restaurants and plan their future reviews.

- **Review**: The Review page enables users to provide ratings and comments for the restaurants they have visited. Once a review is submitted, the entry is removed from the visited database and added to the reviewed entries, maintaining an organized and efficient user experience.

- **History**: The History page displays a comprehensive list of all the restaurants the user has reviewed. It serves as a convenient reference for the user to revisit their favorite places or share recommendations with others.

- **User Authentication**: Better Foods includes pages for user registration, signing in, and logging out to maintain a userbase. Proper input validation and password matching ensure a secure and reliable user experience.

## Installation

1. Clone the repository from [GitHub](https://github.com/dem0nsl4yer/Better_Foods).
2. Install the necessary dependencies using the following command: pip install -r requirements.txt
3. Run the application using the command:python app.py
4. Access the website locally at [http://localhost:5000](http://localhost:5000).

## Usage

1. Register an account or sign in if you already have one.
2. Use the Search page to enter a location and explore nearby restaurants.
3. Click on a restaurant to view more details and top reviews.
4. Visit a restaurant to save it for later review.
5. Review a visited restaurant by providing a rating and comments.
6. Access your reviewed restaurants in the History page.
7. Log out when you're done.

## Contributing

Contributions are welcome! If you have any suggestions or improvements, feel free to open an issue or submit a pull request on [GitHub](https://github.com/your-username/better-foods).

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

