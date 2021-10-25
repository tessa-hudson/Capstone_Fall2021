# Groups

Groups are a collection of attendees within a particular event. Each group may earn points in the event which are shown on the event's scoreboard.

## Data Model

Name | Type  | Description 
---- | ---- | -----------
`group_id` | UUID | Used to uniquely identify the group. Generated upon creation.
`event_id` | UUID | The event that the group belongs to and subsequently is competing in.
`group_name` | string | The name of the group.
`total_points` | int | The number of points the group has earned in the event. Defaults to 0 upon creation.
`attendess` | [ UUID ] | *Association* A list of UUIDs representing the attendees in the group. Defaults to `[]` upon creation.

## Endpoints

### GET /groups

**Description:** Lists all groups. Outputs group_id, group_name, event_id, total_points of each.

**Authentication:**

**Request Example:**
```
GET /groups
Accept: application/vnd.api+json
```

**Response Example:**
```
HTTP/1.1 200 OK
Content-Type: application/vnd.api+json
{
    "groups": [
        {
            "event_id": "F2DACF22-9D82-4A4B-9853-5FC8DDA47EDB",
            "group_id": "2EDC3F13-984C-40F6-AE3B-21F97730F2BF",
            "total_points": 0,
            "group_name": "Group 1"
        },
        {
            "event_id": "F2DACF22-9D82-4A4B-9853-5FC8DDA47EDB",
            "group_id": "EE8911AD-C455-45D2-9849-268259080C96",
            "total_points": 0,
            "group_name": "Group 2"
        }
    ]
}
```

### POST /groups

**Description:** Request to add an group. When successful, server responds with a status of 200 and the group_id, group_name, event_id, total_points (0), and attendees (empty list). If one of the required fields is missing, the server will respond with a status of 422 and a message indicating that there was missing data for a required field. If no data is provided, the server will respond with a status of 400 and a message indicating that there was no input data provided. 

**Required Fields:** `group_name`, `event_id`

**Authentication:**

**Request Example:**
```
POST /groups
Content-Type: application/json
Accept: application/vnd.api+json

{
    "event_id": "F2DACF22-9D82-4A4B-9853-5FC8DDA47EDB",
    "group_name": "Group 1"
}
```

**Response Example:**
```
HTTP/1.1 200 OK
Content-Type: application/vnd.api+json
{
    "event_id": "f2dacf22-9d82-4a4b-9853-5fc8dda47edb",
    "group_id": "2edc3f13-984c-40f6-ae3b-21f97730f2bf",
    "total_points": 0,
    "attendees": [],
    "group_name": "Group 1"
}
```

### GET /groups/`group_id`

**Description:** Gets the group with the given `group_id`. If the group exists, the server will respond with a status of 200 and the group's group_id, group_name, event_id, total_points, and attendees. If a group with `group_id` does not exist, ther server will respond with a status of 404 and a message indicating that no group exists with that id.

**Parameters:** `group_id`

**Authentication:**

**Request Example:**
```
GET /group/2EDC3F13-984C-40F6-AE3B-21F97730F2BF
Accept: application/vnd.api+json
```

**Response Example:**
```
HTTP/1.1 200 OK
Content-Type: application/vnd.api+json
{
    "attendees": [],
    "group_name": "Group 1",
    "group_id": "2EDC3F13-984C-40F6-AE3B-21F97730F2BF",
    "total_points": 0,
    "event_id": "F2DACF22-9D82-4A4B-9853-5FC8DDA47EDB"
}
```

## POST /groups/`group_id`

**Description:** Request to update the group with the given `group_id`. When successful, the server will respond with a status of 200 and the group's group_id, group_name, event_id, total_points, and attendees with the changes made. If no group exists with the given `group_id`, the server will respond with a status of 404 and a message indicating that no group exists with that id. 

*Note* - When `attendees` is updated, a list of attendee_ids should be included. New attendees will be added to the group via an associated attendee_group_link table. Any attendees that are already in the group will not be duplicated.

**Parameters:** `group_id`

**Allowed fields** `event_id`, `group_name`, `total_points`, `attendees`

**Authentication:**

**Request Example:**
```
POST /groups/2EDC3F13-984C-40F6-AE3B-21F97730F2BF
Content-Type: application/json
Accept: application/vnd.api+json
{
    "total_points": 4,
    "attendees": [
        "8C8905B1-52DE-44F6-93AD-046F39C76CF7",
        "DE97B22F-7EF0-4FD2-AFAC-1A9E5CFE329A"
    ]
}
```

**Response Example:**
```
HTTP/1.1 200 OK
Content-Type: application/vnd.api+json
{
    "attendees": [
        "{'attendee_id': '8C8905B1-52DE-44F6-93AD-046F39C76CF7'}",
        "{'attendee_id': 'DE97B22F-7EF0-4FD2-AFAC-1A9E5CFE329A'}"
    ],
    "group_name": "Group 1",
    "group_id": "2EDC3F13-984C-40F6-AE3B-21F97730F2BF",
    "total_points": 4,
    "event_id": "F2DACF22-9D82-4A4B-9853-5FC8DDA47EDB"
}
```

### DELETE /groups/`group_id`

**Description:** Request to delete the group with the given `group_id`. When successful, the server will respond with a status of 200. If no group exists with the given `group_id`, the server will respond with a status of 404 and a message indicating that no group exists with that id. 

**Parameters:** `group_id`

**Authentication:**

**Request Example:**
```
DELETE /groups/2EDC3F13-984C-40F6-AE3B-21F97730F2BF
```

**Response Example:**
```
HTTP/1.1 200 OK
```
