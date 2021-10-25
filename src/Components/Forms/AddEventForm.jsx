import React, { Component } from 'react'
import { Button, TextField } from '@mui/material'
import LocalizationProvider from "@mui/lab/LocalizationProvider";
import AdapterDateFns from '@mui/lab/AdapterDateFns';
import MobileDatePicker from '@mui/lab/MobileDatePicker';
import '../../Styles/AddEventForm.css'

class AddEventForm extends Component {
    constructor(props) {
        super(props)
        this.state = {eventName: '', eventType: '', startDate: new Date(), endDate: new Date()}

        this.handleChange = this.handleChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
        this.handleStartDateChange = this.handleStartDateChange.bind(this)
        this.handleEndDateChange = this.handleEndDateChange.bind(this)
    }

    handleStartDateChange(event) {
        this.setState({startDate: event})
    }

    handleEndDateChange(event) {
        this.setState({endDate: event})
    }

    handleChange(event) {
        const target = event.target
        const value = target.value
        const name = target.name

        this.setState({
            [name]: value
        })
    }

    handleSubmit(event) {
        event.preventDefault() //This prevents the page from refreshing on submit
        let startDate=this.state.startDate.getDate() + "-"+ parseInt(this.state.startDate.getMonth()+1) +"-"+this.state.startDate.getFullYear();
        let endDate=this.state.endDate.getDate() + "-"+ parseInt(this.state.endDate.getMonth()+1) +"-"+this.state.endDate.getFullYear();
        const obj = {name: this.state.eventName, type: this.state.eventType, startDate: startDate, endDate: endDate}
        const json = JSON.stringify(obj);
        console.log(json);

        // fetch('http://localhost:5000/events', {
        // method: 'POST',
        // mode: 'cors',
        // headers: {
        //     'Content-Type': 'application/json',
        //     'Access-Control-Allow-Origin': '*',
        //     'Accept': '*/*'
        // },
        // body: json,
        // })
        // .then(response => response.json())
        // .then(data => {
        // console.log('Success:', data);
        // })
        // .catch((error) => {
        // console.error(error);
        // });
    }



    render() {
        return (
            <div className="AddEvent">
                <h3>Use this form to add a new event!</h3>
                <form onSubmit={this.handleSubmit}>
                    <TextField 
                        id="eventName" 
                        name="eventName"
                        label="Event Name" 
                        variant="outlined" 
                        value={this.state.eventName} 
                        onChange={this.handleChange} 
                        margin="normal"
                    />
                    <TextField 
                        id="eventType"
                        name="eventType" 
                        label="Event Type" 
                        variant="outlined" 
                        value={this.state.eventType} 
                        onChange={this.handleChange} 
                        margin="normal"
                    />
                    <br />
                    <LocalizationProvider dateAdapter={AdapterDateFns}>
                        <MobileDatePicker
                            label="Start Date"
                            inputFormat="MM/dd/yyyy"
                            value={this.state.startDate}
                            onChange={this.handleStartDateChange}
                            renderInput={(params) => <TextField {...params} />}
                        />
                    </LocalizationProvider>
                    <LocalizationProvider dateAdapter={AdapterDateFns}>
                        <MobileDatePicker
                            label="End Date"
                            inputFormat="MM/dd/yyyy"
                            value={this.state.endDate}
                            onChange={this.handleEndDateChange}
                            renderInput={(params) => <TextField {...params} />}
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
}

export default AddEventForm 