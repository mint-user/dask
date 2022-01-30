# Dask

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
| valid email,<br/>valid password                                   | 201  | OK. __User has been created__                                                                                                                                                        |
| valid email,<br/>valid password,<br/> user with this email exists | 202  | Email is already used                                                                                                                                                                |
| email & password are not valid                                    | 409  | Email should contain "@" <br/> Password is too short<br/>Password is too long<br/>Password should contain uppercase, lowercase letters and numbers<br/>__User has not been created__ |
| no email or password fields                                       | 409  | Request should contain "email" and "password" fields<br/>__User has not been created__                                                                                               |

```json
{
  "error": "Email should contain '@'"
}
```
**PUT** - update account
```json
{
  "user_id": 1,
  "token": "fgdfgdfgfdg",
  "email": "qwe@dask.ru",
  "password": "f43rew32"
}
```

| code | desc                                                                                                                                         |
|------|----------------------------------------------------------------------------------------------------------------------------------------------|
| 200  | OK. User has been updated                                                                                                                    |
| 401  | Unauthorized                                                                                                                                 |
| 409  | Email should contain "@" <br/> Password is too short<br/>Password is too long<br/>Password should contain uppercase, lowercase letters and numbers |

```json
{
  "error": "Email should contain '@'"
}
```
### Login / Sign In