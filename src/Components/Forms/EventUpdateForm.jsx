import React, { useState } from 'react'
import { Button, TextField } from '@mui/material'
import LocalizationProvider from "@mui/lab/LocalizationProvider";
import AdapterDateFns from '@mui/lab/AdapterDateFns';
import MobileDatePicker from '@mui/lab/MobileDatePicker';
import '../../Styles/AddGroupForm.css'
import { useAuth0 } from '@auth0/auth0-react'
import { useLocation } from 'react-router';

const request_url = process.env.REACT_APP_API_REQUEST_URL;

export default function EventUpdateForm(props) {
   const location = useLocation()
   const event = location.state[1]
   const [eventName, setEventName] = useState(event.event_name)
   const [eventType, setEventType] = useState(event.event_type)
   const [startDate, setStartDate] = useState(new Date())
   const [endDate, setEndDate] = useState(new Date())
   
   console.log(event.event_id)
    
    const {getAccessTokenSilently} = useAuth0()

    const handleEventSubmit = (e) => {
        e.preventDefault() //This prevents the page from refreshing on submit
        let formattedStartDate=startDate.getFullYear() + "-"+ parseInt(startDate.getMonth()+1) +"-"+startDate.getDate();
        let formattedEndDate=endDate.getFullYear() + "-"+ parseInt(endDate.getMonth()+1) +"-"+endDate.getDate();
        const obj = {event_name: eventName, event_type: eventType, start_date: formattedStartDate, end_date: formattedEndDate}
        const json = JSON.stringify(obj);
        console.log(json);

        getAccessTokenSilently()
        .then(accessToken => fetch(`${request_url}/events/${event.event_id}`, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Accept': '*/*',
            'Authorization': `Bearer ${accessToken}`
        },
        body: json,
        }))
        .then(response => response.json())
        .then(data => {
        console.log('Success:', data);
        })
        .catch((error) => {
        console.error(error);
        });

        setTimeout(function(){window.location.href= "/events"}, 1000)
    }

        return (
            <div className="AddGroup" style={{maxWidth:'80%', margin:'0 auto'}}>
               <h3>Please update the fields for the event: {event.event_name}!</h3>
               <form onSubmit={handleEventSubmit}>
                <TextField 
                    id="eventName" 
                    name="eventName"
                    label="Event Name" 
                    variant="outlined" 
                    value={eventName} 
                    onChange={e => setEventName(e.target.value)} 
                    margin="normal"
                />
                <TextField 
                    id="eventType"
                    name="eventType" 
                    label="Event Type" 
                    variant="outlined" 
                    value={eventType} 
                    onChange={e => setEventType(e.target.value)} 
                    margin="normal"
                />
                <br />
                <LocalizationProvider dateAdapter={AdapterDateFns} className="datepicker">
                    <MobileDatePicker
                        label="Start Date"
                        inputFormat="MM/dd/yyyy"
                        value={startDate}
                        onChange={e => setStartDate(e)}
                        renderInput={(params) => <TextField {...params} />}
                    />
                </LocalizationProvider>
                <LocalizationProvider dateAdapter={AdapterDateFns} >
                    <MobileDatePicker
                        label="End Date"
                        inputFormat="MM/dd/yyyy"
                        value={endDate}
                        onChange={e => setEndDate(e)}
                        renderInput={(params) => <TextField {...params} />}
                        className="datepicker"
                    />
                </LocalizationProvider>
                <br />
                <Button type="submit" value="Submit" variant="contained"> 
                    Submit
                </Button>
            </form>
            </div>
        )
}

