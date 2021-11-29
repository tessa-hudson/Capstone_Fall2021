from api.Conns.AttendeeConn import ac
from api.Conns.EventConn import ec
from api.Conns.GroupConn import gc

attendees = [
   {"attendee_id": "8cd04c69-9313-4c00-b86e-67da76326986", "firstname": "Attendee", "lastname": "A"},
   {"attendee_id": "02c2b89b-6651-4bef-b82a-ab02087ab0c1", "firstname": "Attendee", "lastname": "B"},
   {"attendee_id": "00fe14ca-7817-4db7-8f88-19e93a99501b", "firstname": "Attendee", "lastname": "C"},
]

def create_attendees():
   for attendee in attendees:
      ac.add_attendee(attendee["attendee_id"], attendee["firstname"], attendee["lastname"])

events = [
   {"event_id": "bc2cb23b-4b78-41ac-8794-12e1050bb428", "event_name": "Event A", "event_type": "Test", "start_date": "2021-10-20", "end_date": "2021-10-21"},
   {"event_id": "417136c4-39c0-4d35-a568-6c0877c267f9", "event_name": "Event B", "event_type": "Test", "start_date": "2021-10-20", "end_date": "2021-10-21"},
   {"event_id": "b261f907-0379-4a3a-8be0-048673721c2e", "event_name": "Event C", "event_type": "Test", "start_date": "2021-10-20", "end_date": "2021-10-21"}
]

def create_events():
   for event in events:
      ec.add_event(event["event_id"], event["event_name"], event["start_date"], event["end_date"], event["event_type"])

groups = [
   {"group_id": "9b994231-63fa-46c0-9782-8ee4425fbd42", "event_id": "bc2cb23b-4b78-41ac-8794-12e1050bb428", "group_name": "Group A", "total_points": 0},
   {"group_id": "655f82ee-5014-477e-9b14-48765d5f0404", "event_id": "bc2cb23b-4b78-41ac-8794-12e1050bb428", "group_name": "Group B", "total_points": 0},
   {"group_id": "0cca813e-8209-42a2-9d8e-dc586473e360", "event_id": "417136c4-39c0-4d35-a568-6c0877c267f9", "group_name": "Group C", "total_points": 0}
]

def create_groups():
   for group in groups:
      gc.add_group(group["group_id"], group["event_id"], group["group_name"], group["total_points"])