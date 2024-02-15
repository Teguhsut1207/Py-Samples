make a backend website app using flask that communicate with frontend throught API.
In this project we use:
1. DB = SQLite3
2. SQLAlchemy
3. py-login for user login and session management (with SQLAlchemy as handler for session database)
4. logger for creating log files
5. py-limitter to give limit on API hit


Available API:
1. register
{
  "name" (minimum 4 chars, must: alphabet,' ',',','.')
  "password" (minimum 8 chars, must: combination of number, alphabet, 1 uppercase, 1 special character)
  "phone_number" (must: number)
  "address" (minimum 10 chars)
  "email" (must: email format)
}

2. login
{
  "email"
  "password"
}

3. profile

4. editprofile
{
  "name" or "address" or "phone_number"
  "password" (mandatory)
}

5. logout
