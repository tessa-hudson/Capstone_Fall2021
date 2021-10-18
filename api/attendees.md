# Attendees

Attendees are the participants in events. They can be added to groups or scored individually. 

## Data Model

Name | Type  | Description 
---- | ---- | -----------
`attendee_id` | UUID | Used to uniquely identify they attendee. Generated upon creation.
`firstname` | string | The attendee's first name
`lastname` | string | Single character. First initial of attendee's lastname.

## Endpoints

### GET /attendees

Description: Lists all attendees

Authentication:

Request Example:
```
GET /attendees
Accept: application/vnd.api+json
```

Response Example:
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
