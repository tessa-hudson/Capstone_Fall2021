import React, { Component } from 'react'
import { Button, TextField } from '@mui/material'
import LocalizationProvider from "@mui/lab/LocalizationProvider";
import AdapterDateFns from '@mui/lab/AdapterDateFns';
import MobileDatePicker from '@mui/lab/MobileDatePicker';
import '../../Styles/AddGroupForm.css'

class Updater extends Component {
    constructor(props) {
        super(props)
        this.state = {
            groupName: '',
            groupId: '',
            eventName: '',
            EventId: '',
            eventType: '',
            startDate: new Date(),
            endDate: new Date(),
            firstName: '',
            lastName: '',
            camperId: '',
        }

        this.handleGroupChange = this.handleGroupChange.bind(this)
        this.handleEventChange = this.handleEventChange.bind(this)
        this.handleStartDateChange = this.handleStartDateChange.bind(this)
        this.handleEndDateChange = this.handleEndDateChange.bind(this)
        this.handleCamperChange = this.handleCamperChange.bind(this)
        this.handleGroupSubmit = this.handleGroupSubmit.bind(this)
        this.handleEventSubmit = this.handleEventSubmit.bind(this)
        this.handleCamperSubmit = this.handleCamperSubmit.bind(this)
    }
    

    handleGroupChange(event) {
        this.setState({groupName: event.target.value})
    }

    handleEventChange(event) {
        const target = event.target
        const value = target.value
        const name = target.name

        this.setState({
            [name]: value
        })
    }

    handleStartDateChange(event) {
        this.setState({startDate: event})
    }

    handleEndDateChange(event) {
        this.setState({endDate: event})
    }

    handleCamperChange(event) {
        const target = event.target
        const value = target.value
        const name = target.name
        
        this.setState({
            [name]: value
        })
    }

    handleGroupSubmit(event) {
        event.preventDefault() //This prevents the page from refreshing on submit
        const obj = {group_name: this.state.groupName}
        const json = JSON.stringify(obj);

        fetch(`https://hbda-tracking-backend.azurewebsites.net/groups/${this.state.groupId}`, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Accept': '*/*'
        },
        body: json,
        })
        .then(response => response.json())
        .then(data => {
        console.log('Success:', data);
        })
        .catch((error) => {
        console.error(error);
        });
    }

    handleEventSubmit(event) {
        event.preventDefault() //This prevents the page from refreshing on submit
        let startDate=this.state.startDate.getFullYear() + "-"+ parseInt(this.state.startDate.getMonth()+1) +"-"+this.state.startDate.getDate();
        let endDate=this.state.endDate.getFullYear() + "-"+ parseInt(this.state.endDate.getMonth()+1) +"-"+this.state.endDate.getDate();
        const obj = {event_name: this.state.eventName, event_type: this.state.eventType, start_date: startDate, end_date: endDate}
        const json = JSON.stringify(obj);

        fetch(`https://hbda-tracking-backend.azurewebsites.net/events/${this.state.eventId}`, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Accept': '*/*'
        },
        body: json,
        })
        .then(response => response.json())
        .then(data => {
        console.log('Success:', data);
        })
        .catch((error) => {
        console.error(error);
        });
    }

    handleCamperSubmit(event) {
        event.preventDefault() //This prevents the page from refreshing on submit
        const obj = {first_name: this.state.firstName, last_name: this.state.lastName}
        const json = JSON.stringify(obj);
        console.log(json);

        fetch(`https://hbda-tracking-backend.azurewebsites.net/attendees/${this.state.camperId}`, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Accept': '*/*'
        },
        body: json,
        })
        .then(response => response.json())
        .then(data => {
        console.log('Success:', data);
        })
        .catch((error) => {
        console.error(error);
        });
    }

    render() {
        const { state } = this.props.location

        if (state[0]==="group") this.state.groupId = state[1].group_id

        if (state[0]==="event") this.state.eventId = state[1].event_id

        if (state[0]==="camper") this.state.camperId = state[1].attendee_id

        return (
            <div className="AddGroup">
                {state[0]==="group" &&
                    <div>
                        <h3>Please update the fields for the group: {state[1].group_name}!</h3>
                        <form onSubmit={this.handleGroupSubmit}>
                            <TextField 
                                id="name" 
                                label="Group Name" 
                                variant="outlined" 
                                value={this.state.groupName} 
                                onChange={this.handleGroupChange} 
                                margin="normal"
                            />
                            <br />
                            <Button type="submit" value="Submit" variant="contained"> 
                                Submit
                            </Button>
                        </form>
                    </div>
                }
                {state[0]==="event" &&
                    <div>
                        <h3>Please update the fields for the event: {state[1].event_name}!</h3>
                        <form onSubmit={this.handleEventSubmit}>
                            <TextField 
                                id="eventName" 
                                name="eventName"
                                label="Event Name" 
                                variant="outlined" 
                                value={this.state.eventName} 
                                onChange={this.handleEventChange} 
                                margin="normal"
                            />
                            <TextField 
                                id="eventType"
                                name="eventType" 
                                label="Event Type" 
                                variant="outlined" 
                                value={this.state.eventType} 
                                onChange={this.handleEventChange} 
                                margin="normal"
                            />
                            <br />
                            <LocalizationProvider dateAdapter={AdapterDateFns} className="datepicker">
                                <MobileDatePicker
                                    label="Start Date"
                                    inputFormat="MM/dd/yyyy"
                                    value={this.state.startDate}
                                    onChange={this.handleStartDateChange}
                                    renderInput={(params) => <TextField {...params} />}
                                />
                            </LocalizationProvider>
                            <LocalizationProvider dateAdapter={AdapterDateFns} >
                                <MobileDatePicker
                                    label="End Date"
                                    inputFormat="MM/dd/yyyy"
                                    value={this.state.endDate}
                                    onChange={this.handleEndDateChange}
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
                }
                {state[0]==="camper" &&
                    <div>
                        <h3>Please update the fields for the camper: {state[1].firstname} {state[1].lastname}!</h3>
                        <form onSubmit={this.handleCamperSubmit}>
                            <TextField 
                                id="firstName" 
                                name="firstName"
                                label="First Name" 
                                variant="outlined" 
                                value={this.state.firstName} 
                                onChange={this.handleCamperChange} 
                                margin="normal"
                            />
                            <br />
                            <TextField 
                                id="lastName" 
                                name="lastName"
                                label="Last Initial" 
                                variant="outlined" 
                                value={this.state.lastName} 
                                onChange={this.handleCamperChange} 
                                margin="normal"
                            />
                            <br />
                            <Button type="submit" value="Submit" variant="contained"> 
                                Submit
                            </Button>
                        </form>
                    </div>
                }
            </div>
        )
    }
}

export default Updater