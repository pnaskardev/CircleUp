# CircleUp - Full Stack Social Media App

CircleUp is a full-stack social media application that allows users to connect, share, and interact with each other through posts, comments, and likes. The app is built using Django Rest Framework for the backend API and Vue.js for the frontend user interface, providing a seamless and engaging social media experience.
## Tech Stack

- **Backend**: Django, Django Rest Framework, Django ORM, Django Channels, Token-based Authentication
- **Frontend**: Vue.js, Vuex, Axios, Bootstrap, Custom CSS
- **Database**: PostgreSQL
- **Deployment**: Heroku, Docker


## Features

- **User Authentication**: CircleUp supports secure user authentication using token-based authentication. Users can create an account, log in, and access personalized profiles.

- **Create and Share Posts**: Users can create and share posts with rich text content, images, and videos. The app supports real-time post creation and editing.

- **Comment and Like Posts**: Users can engage with posts by leaving comments and liking them. Real-time notifications keep users updated on new comments and likes.

- **Real-time Notifications**: CircleUp leverages Django Channels to provide real-time notifications for new posts, comments, and likes, enhancing user engagement.

- **User Profiles**: Each user has a personalized profile page that displays their posts and user information. Users can view and interact with other users' profiles.

- ****



## Run Locally

Clone the project

```bash
  git clone https://github.com/pnaskardev/CircleUp.git
```

Go to the project directory

```bash
  cd CircleUp
```
Install venv

```bash
  pip install venv
```

Create a python virtual environement

```bash
  python -m venv venv
```

Start the virtual environement

```bash
  venv\Scripts\activate
```

install required packages

```bash
  pip install -r requirements.txt
```
Create and migrate the database:
```bash
    python manage.py makemigrations
    python manage.py migrate
```
Start the Server
```bash
  python manage.py runserver
```

**In a seperate terminal** 
Go to the frontend directory

```bash
cd frontend
npm install
```

Start the React development server:
```bash
npm start

```

Access the App at 

```bash
  http://127.0.0.1:3000/
```


## Screenshots



## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

Please adhere to this project's `code of conduct`.


## Authors

- [@pnaskardev](https://www.github.com/pnaskardev)

