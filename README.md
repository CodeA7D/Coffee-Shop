Application Programming 2 Project proposal
Team members:
1. Ahmad Mosa Index: 21-303
2. Osman Emad Index: 16-408
3. Abdulqayyum Yassin Index: 21-308
Project Idea
Our project is an online coffee store web-site designed to make
ordering from an existing coffee store simple and convenient.
Customers are allowed to browse, search and filter the menu,
interact with products, rate and review products, save favorite
products, create an account, and manage their profiles. While
administrators will manage products, inventory, and customer
reviews. The goal of the project is to provide users with a smooth
and enjoyable online coffee store experience by helping them
quickly find products and access detailed information about each
product.
Tech Stack
• FrontEnd: The frontEnd will be developed using HTML, CSS,
and JavaScript to provide a responsive and interactive user
interface.
• Backend: The backend will be implemented using the Django
framework to handle user authentication, business logic, and
communication with the database.
• Database: For the database we will use MySQL to store user
accounts, products, favorites, reviews, and other application
data.
• Database Access: Django ORM will be used to perform
database operations and manage data efficiently.
• Authentication: User authentication and authorization will be
handled using Django's built-in Authentication System.
• AJAX: The website will use AJAX, implemented through the
JavaScript Fetch API, to update data dynamically without
reloading the page.
• Version Control: The project will be managed using Git and
hosted on GitHub for collaboration and version control.
Features List
• User Management: Users can create an account, log in, log out,
and securely access their personal dashboard. Customers can
update their profile information, while administrators will
access a dashboard that provides quick access to product
management, inventory management, and customer review
moderation.
• Store Menu: Coffee and Snack products are displayed as
interactive cards showing the product image, price, availability,
rating, and favorite status. Each Product has a dedicated details
page containing additional information, ingredients, and
customer reviews.
• Favorite & Recommendation System: Logged-in users can add
or remove Products from their favorites. The homepage
recommends the most popular products based on total number
of logged-in users who marked each product as favorite.
• Search, Sorting & Filtering: Users can search for products, sort
them by price, rating or favorite count. Users can also filter
them by category or availability.
• Reviews & Ratings: Customers can submit ratings and reviews
for products. Average ratings are automatically calculated and
displayed for each Product.
• Store Management (Admin): Administrators can create,
update, and delete products, manage inventory information,
update prices and discounts, and moderate customer reviews.
Ajax Features:
We will improve the coffee store website by using AJAX as we
learned to make the user experience smoother and more
interactive. Instead of reloading the entire page whenever a user
searches for a product or updates their profile, the website will
communicate with the server in the background and display the
changes instantly. This will make the application feel faster and
more responsive.
Feature 1: Live Search Suggestions
The search bar will use AJAX call to provide live search results
while the user is typing. Every time the user enters a letter, the
website will send a request to the server and retrieve matching
products. The matching results will appear immediately below the
search box without refreshing the page. This helps users find the
products they are looking for more quickly.
Feature 2: User Profile Updates
Users will be able to edit their profile information, such as their
name or email address, without leaving the current page. When
they click the Save button, an AJAX request will send the updated
information to the server in the background. If the update is
successful, the website will display a confirmation message and
refresh only the profile information instead of reloading the entire
page. This makes updating account details faster and provides a
better overall user experience.
Feature 3: Filter Menu by Category
Users click categories like cold drinks, hot drinks and Snack. Only
matching items are displayed instantly. No page refresh is needed.
Feature 4: Sort Menu by Price
This feature will use AJAX to sort menu items by price without
refreshing the page. When the user selects a sorting option such
as sorting by price, rating or favorite counts. the menu updates
instantly to display the products in the chosen order, making it
easier to browse and compare between items.
