### Title of project: **Gamebu**

### Project description: This project is my first full-size back-end project on django python.
Gamebu - collected view of some sites, main functional is blog, where people can post some card-post with
text, images or combine content. Site functional include oportunity of registration and comment some posts,
checking the author page.
This project maked on Django because its final project of my learning of python language in this time.

### List of contents:

- [X] Registration

![Registration](https://github.com/Limon8bit/Gamebu/blob/main/README/registration%20page.png)

- [X] Login

![Login](https://github.com/Limon8bit/Gamebu/blob/main/README/login_page.png)

- [X] Logout

![Login/logout changes](https://github.com/Limon8bit/Gamebu/blob/main/README/User%20interface%20changes%20after%20login.png)

- [X] Post some posts with text/image/combine this two.

![Another posts](https://github.com/Limon8bit/Gamebu/blob/main/README/some%20types%20of%20posts.png)

- [X] Comment posts

![Post with comment](https://github.com/Limon8bit/Gamebu/blob/main/README/postpage%20with%20comment.png)

- [X] Check the author page using link from post or comment

- [X] Search posts with title or text content with search field

![Search](https://github.com/Limon8bit/Gamebu/blob/main/README/search%20system%20work.png)


### List of future contents:

- Rating system
- Rework of GET posts system with using new rating system
- Layers system of comments
- Add tags system

### How to install and run:

After download this project you must install docker and run this. Change the CSRF trusted ips in settings of the project to your own IP like this actually is. Enter the project directory (../Gamebu/blog) and run command `docker-compose up -d` after complete this proces use command `docker-compose ps` for check state of docker images (web, postgres, nginx). If its state is UP all is good. For create `admin-user` use command `docker exec -it blog_web_1 bin/bash` to enter the project environment. Next use command `python manage.py createsuperuser` and enter the parameters of your admin-user (you can use any slug, but recommended to use username in lowercase). Last step: connect to project with yours browser `http://yourdomen.yourip/admin`, enter username and password of your admin-user and create objects of `sexs table`. Complete!
