import React, { useState } from 'react'
import { Button, TextField } from '@mui/material'
import LocalizationProvider from "@mui/lab/LocalizationProvider";
import AdapterDateFns from '@mui/lab/AdapterDateFns';
import MobileDatePicker from '@mui/lab/MobileDatePicker';
import '../../Styles/AddEventForm.css'
import { useAuth0 } from '@auth0/auth0-react'

const request_url = process.env.REACT_APP_API_REQUEST_URL;

function AddEventForm(props) {

    const [eventName, setEventName] = useState('')
    const [eventType, setEventType] = useState('')
    const [startDate, setStartDate] = useState(new Date())
    const [endDate, setEndDate] = useState(new Date())

    const {getAccessTokenSilently} = useAuth0()


    const handleSubmit = (event) => {
        event.preventDefault() //This prevents the page from refreshing on submit
        let formattedStartDate=startDate.getFullYear() + "-"+ parseInt(startDate.getMonth()+1) +"-"+startDate.getDate();
        let formattedEndDate=endDate.getFullYear() + "-"+ parseInt(endDate.getMonth()+1) +"-"+endDate.getDate();
        const obj = {event_name: eventName, event_type: eventType, start_date: formattedStartDate, end_date: formattedEndDate}
        const json = JSON.stringify(obj);
        console.log(json);

        getAccessTokenSilently()
        .then(accessToken => fetch(`${request_url}/events`, {
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
    }




    return (
        <div className="AddEvent">
            <h3>Use this form to add a new event!</h3>
            <form onSubmit={handleSubmit}>
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

export default AddEventForm 