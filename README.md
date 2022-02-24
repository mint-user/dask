# Dask
poetry run python run.py

## Models

### Account

| id  | email       | password        | token   | token_expires       |
|-----|-------------|-----------------|---------|---------------------|
| 1   | qwe@dask.ru | f43reпg54yehw32 | rt4r23r | 2022-02-23 23:12:12 |

### Task

| id  | user_id | parent_id | description |
|-----|---------|-----------|-------------|
| 1   | 1       | NULL      | Global task |
| 2   | 1       | 1         | Subtask     |

## Endpoints

### Registration / Sign Up

/api/v1/accounts

**POST** - create new user
```json
{
  "email": "qwe@dask.ru",
  "password": "f43rew32"
}
```
| action                                                            | code | expected                                                                                                                                                                             |
|-------------------------------------------------------------------|------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| no email or password fields                                       | 400  | Request should contain "email" and "password" fields<br/>__User has not been created__                                                                                               |
| email or password are not valid                                   | 400  | Email should contain "@" <br/> Password is too short<br/>Password is too long<br/>Password should contain uppercase, lowercase letters and numbers<br/>__User has not been created__ |
| valid email,<br/>valid password                                   | 201  | OK. __User has been created__                                                                                                                                                        |
| valid email,<br/>valid password,<br/> user with this email exists | 406  | Email is already used                                                                                                                                                                |

```json
{
  "error": "Email should contain '@'"
}
```

### Login / Sign In
#### POST - getting token
/api/v1/accounts/login
```json
{
  "email": "qwe@qwe",
  "password": "123"
}
```

#### Tests
Setup - exists user qwe@qwe oIwi5jdPJlLGzba

| method | request                                                         | response                                                                                                         | code | desc                                                                 |
|--------|-----------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|------|----------------------------------------------------------------------|
| POST   | {"email": "qwewasd@qwe1111", "password": "1"}                   | {"error":"Wrong email or password"}                                                                              | 400  | wrong email                                                          |
| POST   | {"email": "qwe@qwe", "password": "123"}                         | {"error":"Wrong email or password"}                                                                              | 400  | wrong password                                                       |
| POST   | {}                                                              | {"error":"Bad request"}                                                                                          | 400  | Bad request                                                          |
| POST   | {"email": "qwe@qwe",<br/>"password": "oIwi5jdPJlLGzba?"}        | {"user": {"id": 1}, <br/>token": "8dfafac23e0382d29627c856156cac8e",<br/>"token_expires": "2022-02-03 23:20:10"} | 201  | OK. User has been logged in. <br/>token_expires - datetime in future |
| DELETE | {}                                                              | {"error":"Bad request"}                                                                                          | 400  | Bad request                                                          |
| DELETE | {"user_id": 45, "token": "8dfafac23e0e"}                        | {"error":"Wrong user ID or token"}                                                                               | 404  | Wrong token                                                          |
| DELETE | {"user_id": 1, <br/>token": "8dfafac23e0382d29627c856156cac8e"} |                                                                                                                  | 200  | OK. User has been logged out                                         |

**PATCH** - update account
* Only with token
* At least one of fields "email" or "password" needed, or both
```json
{
  "user_id": 1,
  "token": "fgdfgdfgfdg",
  "email": "qwe@dask.ru",
  "password": "f43rew32"
}
```

| action                                                            | code | expected                                                                                                                                                                             |
|-------------------------------------------------------------------|------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| different valid email,<br/>different valid password               | 200  | OK. __User has been updated__                                                                                                                                                        |
| valid email,<br/>valid password,<br/> user with this email exists | 202  | Email is already used                                                                                                                                                                |
| email & password are not valid                                    | 409  | Email should contain "@" <br/> Password is too short<br/>Password is too long<br/>Password should contain uppercase, lowercase letters and numbers<br/>__User has not been created__ |
| no email or password fields                                       | 409  | Request should contain "email" and "password" fields<br/>__User has not been created__                                                                                               |

| code | desc                                                                                                                                               |
|------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| 200  | OK. User has been updated                                                                                                                          |
| 401  | Unauthorized                                                                                                                                       |
| 409  | Email should contain "@" <br/> Password is too short<br/>Password is too long<br/>Password should contain uppercase, lowercase letters and numbers |

```json
{
  "error": "Email should contain '@'"
}
```
