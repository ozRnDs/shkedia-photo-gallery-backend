## 0.1.0 (2023-12-03)

### Feat

- **templates/albums,templates/view_album**: Activate the next and previous buttons
- **templates/view_media**: Display the user and device information. Add back button
- **gallery_service**: Add the full user and device data in get_media_content function
- **templates/about_media**: Create a section about the media's lifecycle
- **templates/about**: Add the page context
- **About**: Add about page and link it to the webservice
- **base/views**: Integrate the auth_service in the private pages
- **business/authentication**: Create custom authentication service that uses the auth API
- **business/db/user_service**: Add retry mechanism to login. Fix search_user signature to complient with auth API
- **src**: Create web app with 3 pages. Albums, Albums Views, Photo View

### Fix

- **GalleryService**: Set the caching retention for production mode
- **base/views**: Send user's real token to the RestAPI operations. Send the user and device data to the view_media page
- **bootstrap.min.css**: Change the img-fluid width to min-width: 100
- **views/about,AuthService**: Add is_authenticated decorator, inorder to display the correct "login"/"logout" button in the navbar

### Refactor

- **templates/footer,navbar**: Personalize the statis imformation in the footer and navbar
- **search**: Enable search only on desired views per demand
- **business/authentication/service**: Set login_redirect_path in the service contructor and not in the decorator
- **django**: Create the django base template
- **Project-Template**: Create the project from template