
# EventOn--backend
Backend API Server 
- FastAPI
- SQLAlchemy
- Sqlite
## Setting up Dev 

```
git clone  <repoID>
cd symetry
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```
### Environment Variables
| NAME | DESC | TYPE | DEFAULT | REQUIRED |
| --- | --- | --- | --- | --- |

### JSON Schema
#### Create User
```
{
 "email": STRING,
 "password": STRING
}
```

#### Create Event
```
{
 "id": STRING
}
```
#### Create Sheet
```
{
 "title": STRING
}

```
#### Token
```
{
 "username": STRING, 
 "password": STRING
}

```
### Endpoints
| URL | DESCRIPTION | METHOD | PARAMS | AUTHENTICATED | RESPONSE |
| --- | --- | --- | --- | --- | --- |
| `/` | Get root information about the API | GET | - | No | - |
| `/token` | Generate token | POST | - | No | [Token](#Token) |
| `/user/` | Create a new User (Registration) | POST | [User](#create-user) | No | [User](#receive-user) |
| `//` | Update Existing User Info | PATCH | [UserUpdate](#update-user) | Yes |  [User](#receive-user) |
| `//` | Soft Delete User by ID | DELETE | - | Yes |  - |
| `//` | Terminates the session | POST | - | Yes | - |
| `/event` | Create a new Event (Registration) | POST | [Event](#create-event) | Yes | [App](#receive-event) |
| `/events` | Get Events  | GET | -| Yes| [Event](#receive-event) |
| `/events` | Delete Events  | DELETE | [Event](#create-event) | No | [Event](#receive-event) |
| `//` | Update Existing Event  | PATCH | [Event](#update-app) | Yes |  [App](#receive-app) |

### Tokens
Token contains 3 parts before encoding with base64(UTF-8)
- user_id, app secret end expire time
