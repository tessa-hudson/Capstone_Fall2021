# Attendees

Attendees are the participants in events. They can be added to groups or scored individually. 

## Data Model

Name | Type  | Description 
---- | ---- | -----------
`attendee_id` | UUID | Used to uniquely identify the attendee. Generated upon creation.
`firstname` | string | The attendee's first name
`lastname` | string | Single character. First initial of attendee's lastname.

## Endpoints

### GET /attendees

**Description:** Lists all attendees. Outputs firstname, lastname, and attendee_id of each.

**Authentication:**

**Request Example:**
```
GET /attendees
Accept: application/vnd.api+json
```

**Response Example:**
```
HTTP/1.1 200 OK
Content-Type: application/vnd.api+json
{ 
   "attendees": [
      {
          "attendee_id": "8C8905B1-52DE-44F6-93AD-046F39C76CF7",
          "lastname": "B",
          "firstname": "Attendee"
      },
      {
          "attendee_id": "DE97B22F-7EF0-4FD2-AFAC-1A9E5CFE329A",
          "lastname": "A"
          "firstname": "Attendee"
      }
   ]
}
```

### POST /attendees

**Description:** Request to add an attendee. When successful, server responds with a status of 200 and the attendee's firstname, lastname, and attendee_id. If one of the required fields is missing, the server will respond with a status of 422 and a message indicating that there was missing data for a required field. If no data is provided, the server will respond with a status of 400 and a message indicating that there was no input data provided. 

**Required Fields:** `firstname`, `lastname`

**Authentication:**

**Request Example:**
```
POST /attendees
Content-Type: application/json
Accept: application/vnd.api+json

{
   "firstname": "Attendee",
   "lastname": "A"
}
```

**Response Example:**
```
HTTP/1.1 200 OK
Content-Type: application/vnd.api+json
{ 
   "attendee":
      {
          "attendee_id": "DE97B22F-7EF0-4FD2-AFAC-1A9E5CFE329A",
          "lastname": "A"
          "firstname": "Attendee"
      }
}
```

### GET /attendees/`attendee_id`

**Description:** Gets the attendee with the given `attendee_id`. If the attendee exists, the server will respond with a status of 200 and the attendee's firstname, lastname, and attendee_id. If and attendee with `attendee_id` does not exist, ther server will respond with a status of 404 and a message indicating that no attendee exists with that id.

**Parameters:** `attendee_id`

**Authentication:**

**Request Example:**
```
GET /attendees/8C8905B1-52DE-44F6-93AD-046F39C76CF7
Accept: application/vnd.api+json
```

**Response Example:**
```
HTTP/1.1 200 OK
Content-Type: application/vnd.api+json
{ 
   "attendee":
      {
          "attendee_id": "8C8905B1-52DE-44F6-93AD-046F39C76CF7",
          "lastname": "B",
          "firstname": "Attendee"
      }
}
```

### DELETE /attendees/`attendee_id`

**Description:** Request to delete the attendee with the given `attendee_id`. When successful, the server will respond with a status of 200. If no attendee exists with the given `attendee_id`, the server will respond with a status of 404 and a message indicating that no attendee exists with that id. 

**Parameters:** `attendee_id`

**Authentication:**

**Request Example:**
```
DELETE /attendees/8C8905B1-52DE-44F6-93AD-046F39C76CF7
```

**Response Example:**
```
HTTP/1.1 200 OK
```

