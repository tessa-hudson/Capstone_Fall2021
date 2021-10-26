import React, { Component } from 'react'
import { Button, TextField } from '@mui/material'
import '../../Styles/AddCamperForm.css'

class AddCamperForm extends Component {
    constructor(props) {
        super(props)
        this.state = {firstName: '', lastNameInitial: ''}

        this.handleChange = this.handleChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
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
        const obj = {firstname: this.state.firstName, lastname: this.state.lastNameInitial}
        const json = JSON.stringify(obj);
        console.log(json);

        fetch('https://hbda-tracking-backend.azurewebsites.net/attendees', {
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
        return (
            <div className="AddCamper">
                <h3>Use this form to add a camper!</h3>
                <form onSubmit={this.handleSubmit}>
                    <TextField 
                        id="firstName" 
                        name="firstName"
                        label="First Name" 
                        variant="outlined" 
                        value={this.state.firstName} 
                        onChange={this.handleChange} 
                        margin="normal"
                    />
                    <br />
                    <TextField 
                        id="lastInitial" 
                        name="lastNameInitial"
                        label="Last Initial" 
                        variant="outlined" 
                        value={this.state.lastNameInitial} 
                        onChange={this.handleChange} 
                        margin="normal"
                    />
                    <br />
                    <Button type="submit" value="Submit" variant="contained"> 
                        Submit
                    </Button>
                </form>
            </div>
        )
    }
}

export default AddCamperForm