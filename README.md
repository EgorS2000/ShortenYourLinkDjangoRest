# Introduction

ShortenYourLink is DRF API, which was built to shorten your long none-presentable link.

These docs describe how to use the [ShortenYourLink](https://app.swaggerhub.com/apis/EgorS2000/ShortenYourLink/v1.0.0) API.

## Features
- NGINX
- Celery and RabbitMQ give ability to check and delete old links every 15 minutes

## Authorization

All API requests require the use of a generated API key.
To authenticate an API request, you should provide your API key in the `Authorization` header.

## Responses

Many API endpoints return the JSON representation of the resources created, edited or deleted. However, if an invalid request is submitted, or some other error occurs, ShortenYourLink returns a JSON response in the following format:

```javascript
{
  "message" : string,
}
```

## Status Codes

ShortenYourLink returns the following status codes in its API:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 400 | `BAD REQUEST` |
| 404 | `NOT FOUND` |
