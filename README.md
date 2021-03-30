# Introduction

ShortenYourLink was built to shorten your long none-presentable link.

## Authorization

All API requests require the use of a generated API key.
To authenticate an API request, you should provide your API key in the `Authorization` header.

## Responses

Many API endpoints return the JSON representation of the resources created, edited or delited. However, if an invalid request is submitted, or some other error occurs, ShortenYourLink returns a JSON response in the following format:

javascript
{
  "message" : string,
}

## Status Codes

ShortenYourLink returns the following status codes in its API:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 400 | `BAD REQUEST` |
| 404 | `NOT FOUND` |
