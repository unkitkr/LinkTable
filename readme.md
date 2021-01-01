# Linktable
#### Linktable is a micro API to create  teams and share/store the importaint links you come across.

#### Features:

 1. Create gropus/teams
 2. Create admin permissions
 3. Share links/importaint messages
 4. Signup/signin
 
#### Dependencies
1. Flask (  `pip install flask`)
2. SQLAlchemy ( `pip install SQLAlchemy` )
3. Flask Login ( `pip install Flask-Login` )

#### Starting the development server

    python app.py  
    python3 app.py (linux)

#### API Structure

##### Signup
/signup
###### Payload (JSON Form data):

|Parameter| Type |Required|Sample Value|
|--|--|--|--|
|full_name| String| Yes| "Ankit"|
|user_email| String | Yes| "importankit@gmail.com"|
|user_password| String| Yes | "Somepassword"|
|user_name| String| Yes | "unkitkr|

##### Signin
/signin
###### Payload (JSON Form data):

|Parameter| Type |Required|Sample Value|
|--|--|--|--|
|user_password| String| Yes | "Somepassword"|
|user_name| String| Yes | "unkitkr|

##### Create Room
/createroom
###### Payload (JSON Form data):

|Parameter| Type |Required|Sample Value|
|--|--|--|--|
|room_name| String| Yes | "Some Name"|


##### Share link
/sendlink
###### Payload (JSON Form data):

|Parameter| Type |Required|Sample Value|
|--|--|--|--|
|link| String| Yes | "Some Name"|
|room_id| String (UUID)| Yes | "Some ID"|
|link_description| String| Yes | "URL, Description"|

##### Get room data
/getroomdata
###### Payload (JSON Form data):

|Parameter| Type |Required|Sample Value|
|--|--|--|--|
|room_id| String (UUID)| Yes | "Some Name"|

##### Join room 
/joinroom
###### Payload
None, just needs to be authenticated.

###### Also do not forget to configure Database URI

