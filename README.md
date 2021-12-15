
# Synchronization

Synchronization is one of the biggest features of StackEdit. It enables you to synchronize any file in your workspace with other files stored in your **Google Drive**, your **Dropbox** and your **GitHub** accounts. This will sync all your files, folders and settings automatically. This will allow you to fetch your workspace on any other device.
	> To start syncing your workspace, just sign in with Google in the menu.

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)
- The file synchronization will keep one file of the workspace synced with one or multiple files in **Google Drive**, **Dropbox** or **GitHub**.
	> Before starting to sync files, you must link an account in the **Synchronize** sub-menu.
# Coverin--backend
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


Tasks will be assigned as "Issues" Check the project board. 

### Tokens
Token contains 3 parts before encoding with base64(UTF-8)
- user_id, app secret end expire time
