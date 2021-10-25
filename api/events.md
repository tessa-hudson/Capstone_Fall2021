# Events

Events are the main focus of the app. Each event has a separate scoreboard and groups added to the event will be added to the scoreboard with a count representing the total points the group has earned.

## Data Model

Name | Type  | Description 
---- | ---- | -----------
`event_id` | UUID | Used to uniquely identify the event. Generated upon creation.
`event_name` | string | The name of the event; subsequently, the name of the scoreboard.
`event_type` | string | A short description of the event (ie camp, meeting, etc).
`start_date` | date | The day the event starts in ISO format: YYYY-MM-DD
`start_date` | date | The day the event ends in ISO format: YYYY-MM-DD

## Endpoints

### GET /events

**Description:** Lists all events. Outputs event_id, event_name, type, start_date and end_date of each.

**Authentication:**

**Request Example:**
```
GET /events
Accept: application/vnd.api+json
```

**Response Example:**
```
HTTP/1.1 200 OK
Content-Type: application/vnd.api+json
{
    "events": [
        {
            "event_id": "F2DACF22-9D82-4A4B-9853-5FC8DDA47EDB",
            "end_date": "2021-10-30",
            "event_name": "New Event",
            "event_type": "Test",
            "start_date": "2021-10-29"
        },
        {
            "event_id": "F811FB42-C609-4A13-BDB2-AC6D7499DE71",
            "end_date": "2022-06-30",
            "event_name": "Camp",
            "event_type": "Camp Clot Not 2022",
            "start_date": "2022-07-11"
        }
    ]
}
```

### POST /events

**Description:** Request to add an event. When successful, server responds with a status of 200 and the event_id, event_name, event_type, start_date, and end_date. If one of the required fields is missing, the server will respond with a status of 422 and a message indicating that there was missing data for a required field. If no data is provided, the server will respond with a status of 400 and a message indicating that there was no input data provided. 

**Required Fields:** `event_name`, `event_type`, `start_date`, `end_date`

**Authentication:**

**Request Example:**
```
POST /events
Content-Type: application/json
Accept: application/vnd.api+json

{
    "end_date": "2022-06-30",
    "start_date": "2022-07-11",
    "event_type": "Meeting",
    "event_name": "New Meeting"
}
```

**Response Example:**
```
HTTP/1.1 200 OK
Content-Type: application/vnd.api+json
{
    "event_id": "01a46ac4-f7b7-4f98-9dd9-15fabc632ab2",
    "end_date": "2022-06-30",
    "event_name": "New Meeting",
    "event_type": "Meeting",
    "start_date": "2022-07-11"
}
```

### GET /events/`event_id`

**Description:** Gets the event with the given `event_id`. If the event exists, the server will respond with a status of 200 and the event's event_id, event_name, event_type, start_date, and end_date. If and event with `event_id` does not exist, ther server will respond with a status of 404 and a message indicating that no event exists with that id.

**Parameters:** `event_id`

**Authentication:**

**Request Example:**
```
GET /events/F811FB42-C609-4A13-BDB2-AC6D7499DE71
Accept: application/vnd.api+json
```

**Response Example:**
```
HTTP/1.1 200 OK
Content-Type: application/vnd.api+json
{
    "event_id": "F811FB42-C609-4A13-BDB2-AC6D7499DE71",
    "end_date": "2022-06-30",
    "event_name": "Camp",
    "event_type": "Camp Clot Not 2022",
    "start_date": "2022-07-11"
}
```

### DELETE /events/`event_id`

**Description:** Request to delete the event with the given `event_id`. When successful, the server will respond with a status of 200. If no event exists with the given `event_id`, the server will respond with a status of 404 and a message indicating that no event exists with that id. 

**Parameters:** `event_id`

**Authentication:**

**Request Example:**
```
DELETE /events/01A46AC4-F7B7-4F98-9DD9-15FABC632AB2
```

**Response Example:**
```
HTTP/1.1 200 OK
```
