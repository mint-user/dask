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
POST
```json
{
  "email": "qwe@dask.ru",
  "password": "f43rew32"
}
```
| code | desc                                                                                                                                               |
|------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| 201  | OK. User has been created                                                                                        |
| 409  | Email should contain "@" <br/> Password is too short<br/>Password is too long<br/>Password should contain uppercase, lowercase letters and numbers |

```json
{
  "error": "Email should contain '@'"
}
```
### Login / Sign In