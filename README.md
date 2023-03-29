# BETTER FOODS
#### Video Demo:  <https://www.youtube.com/watch?v=HA6ljpb-dPA>
#### Description:
This is a website built around Google maps and Yelp APIs with the idea to filter out good restaurants around a locality with respective ratings, and create a personal database with users own ratings and comments.
It has multiple pages namely:
Search - this is lifeline of the website, where maximal user interaction occurs. User searches a particular location, and the API calls to Google Maps and Yelp create tables with all the outputs.
The co-ordinates of the place are back-calculated by calling in the GEOCODE API, a derivative of Google Maps. These coordinates are then employed to fetch the nearby restaurants within 1000M in both Google Places API and the YELP API. YELP API fortunately, can calculate these metrics directly by using the approximate location string.
These outputs have been filtered out with rating calls and also provide estimates from origin location by employing Haversine method. Both API calls occur simultaneously and we filter out the particular parameters that are needed for further assignment namely: the operational status of the restaurant as in they are closed or not; the address of the particular place; the key NAME of the particular place; the averaged rating for the place; the price level from 1-5; and the distance between the keyed in place and the particular restaurant.
The distance between the particular search query and the restaurant in question is calculated by employing the haversine function. This function basically pulls in the co-ordinates of the two places and calculates the distance in meters in this particular implementation.
Details - The user then, has the option to dive deeper, and see further detail such as 3-5 top reviews and restaurant’s website.
Visit- Once the user decides to visit a particular restaurant, this page/database stores these entries till the user wishes to review the particular place with their rating and the respective comments.
Review- Once the user reviews a particular restaurant, it deletes the entry from visited database and adds it onto the reviewed entries. This is done, in order to let the user, create a database of entries that have been visited, but have still not been reviewed.
History- These entries then are always available to the user in the History page, OR the homepage. This is useful, as it provides a shorthand display of all the restaurants that the user really likes in case they wish to visit some particular place again.
Around this there are pages for registering/signing in/logout employed to maintain a userbase. Registration mandates the user to provide proper inputs and performs the re-check for contingency in case password is mismatched.
As we are employing global variables, on logging out all the variables are essentially re set in order to not cause any anomalies when users login back and forth during traffic.
All the entries saved in by the user are handled by the SQLITE3 database. Herein, we have employed the C, R, U, D principles of creating TABLES, Reading into tables, Updating tables and Deleting entries as and when database entries need to be updated.


