## converse-Ecom
## Features:
- FastAPI project structure tree
## Table Model
  **User**
        - **id**, **name**, **email**, **password**, **phone_number**,**created_at**,**otp**, **expires_at**, **is_active** ,**roles**, **refresh_token**(roles Relation to the **UserRole** table)
   **Role**
        - **id**, **name**, **email**,**user**(user Relation to the **UserRole** table)
   **UserRole**
    - **user_id**, **role_id**, **user**,**role**(user and Relation to the **User** table and **Role** table)
- database => sqlite
- authentication => JWT Autentication

## Structured Tree
```
├── fastapi
│   ├── project
│   │   ├── core
│   │   │    ├──__init__.py
│   │   │    ├──auth.py     # Contains auth functionality like  validations,
│   │   │    └──config.py   # Contains core functionality like send_otp ,
│   │   ├── routers   # Contains modules for  (API ROUTER).
│   │   │    ├── __init__.py
│   │   │    ├──Role.py				#  Contains role functionality like Admin ,manager
│   │   │    └──User.py				# Contains user functionality like Singin ,Login
│   │   ├── crud.py				# Contains crud functionality like database management
│   │   ├── database.py  	 #Contains database functionality like database connection
│   │   ├── dependency.py
│   │   ├── main.py     # Initializes the FastAPI app and brings together various components.
│   │   ├── models      # Contains modules defining database models for Users,Role UserRole.
│   │   ├── __init__.py
│   │   ├── schemas.py   # Pydantic model for data validation
│   │    ├── requirements.txt # Lists project requirements
```
**/user/create-otp**: Api used to Create User by Signin **(post)**
**/user/verify-otp**:Api used to Verify the User to  Signin once the otp verfied then the user created **(put)**
**/user/login**: Api used to Login once otp is valid then user login and get token **(put)**
**/user/login**: Api used to Login and get Tokens **(post)**
 
**/user/request_otp**: Api used to  request get otp to login **(post)**
**/user/refresh_token/**: Api used to create a Access Token **(post)**
 

**/user/change_password/**: Api used to Change The Password after Login  **(put)**
**/user/logout/**:Api used to logout **(delete)**
**/user/single/user/{user_id}**:Api used to Get the Single user Data **(get)**
**/user/all/**:Api used to Get the all the User **(get)**
**/user/user/{user_id}**:Api used to delete the Single user Data **(delete)**
**/user/email_To_Forget_Password**:Api used to Change passwords if the user Forget the Password user Verification by the Email **(put)**
**/user/otp_verify**: Api used to verify the otp Allow user Change Password in Forget Password **(post)**
**/user/change_froget_password**: Api perform , once the user verify the otp  user Allowed to  Change Password  in fileds for new_password **(put)**
**/user/create/User_Role**:Api used to create a User with Role Manually by  Anotheruser **(post)**
**/user/user/{user_id}**:Api used to update the created User with Role Manually by  Anotheruser **(put)**
**/Role/create/role**:Api used to Create the Role  **(post)**
# Setup
Creat folder by the Structured Tree

Create a virtual environment to install dependencies in and activate it:
```sh
$ python -m venv venv
$ source venv/bin/activate
```
Then install the dependencies:
```sh
# for this to Install all library at once
(venv)$ pip install -r requirements.txt
#other wise install all the packages manually
(venv)$ pip install fastapi
(venv)$ pip install bycrpt
(venv)$ pip install uvicorn
(venv)$ pip install PyJWT python-jose
(venv)$ pip install pydantic
(venv)$ pip install passlib
(venv)$ pip install SQLAlchemy
(venv)$ pip install alembic

```
Once `pip` has finished downloaded you installed all the requirement:
To Run the Api  `**uvicorn project.main:app --reload**`

# Tools
### Back-end
#### Language:
    Python above(3.7)
#### Frameworks:
    FastAPI

#### Other libraries / tools:
    SQLAlchemy
 
    pydantic
    starlette
    uvicorn
    python-jose
    bycrpt
    pyJWT
    passlib
## Thank You
