### Flask app with MongoDB and docker-compose.

Allows you to create, update, and read key-value pairs via HTTP requests.

*APPLICATION LAUNCH*

`docker-compose up --build`

*APPLICATION USING*

Greeting
```http request
GET / HTTP/1.1
Host: localhost:8080
Content-Type: application/json
```

Create key-value
```http request
POST /api/keyvalue HTTP/1.1
Host: localhost:8080
Content-Type: application/json

{
    "key": "your_key",
    "value": "your_value"
}
```

Update key-value
```http request
PUT /api/keyvalue/<key> HTTP/1.1
Host: localhost:8080
Content-Type: application/json

{
    "value": "your_new_value"
}
```

Get key-value
```http request
GET /api/keyvalue/<key> HTTP/1.1
Host: localhost:8080
Content-Type: application/json
```
