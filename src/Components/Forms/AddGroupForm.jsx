import React, { Component } from 'react'
import { Button, TextField } from '@mui/material'
import '../../Styles/AddGroupForm.css'

class AddGroupForm extends Component {
    constructor(props) {
        super(props)
        this.state = {groupName: ''}

        this.handleChange = this.handleChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    handleChange(event) {
        this.setState({groupName: event.target.value})
    }

    handleSubmit(event) {
        event.preventDefault() //This prevents the page from refreshing on submit
        const obj = {group_name: this.state.groupName, event_id: "F811FB42-C609-4A13-BDB2-AC6D7499DE71"}
        const json = JSON.stringify(obj);
        console.log(json);

        fetch('http://localhost:5000/groups', {
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
            <div className="AddGroup">
                <h3>Use this form to add a new group!</h3>
                <form onSubmit={this.handleSubmit}>
                    <TextField 
                        id="name" 
                        label="Group Name" 
                        variant="outlined" 
                        value={this.state.groupName} 
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

export default AddGroupForm