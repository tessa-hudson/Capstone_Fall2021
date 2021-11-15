import React, { Component } from 'react'
import { Button, Grid } from '@mui/material'
import '../Styles/GetCampers.css'

class GetCampers extends Component {
    constructor(props) {
        super(props)
        this.state = {Campers: []}

        this.handleSubmit = this.handleSubmit.bind(this)
        this.deleteCamper = this.deleteCamper.bind(this)
    }

    handleSubmit(event) {
        event.preventDefault() //This prevents the page from refreshing on submit
        fetch('https://hbda-tracking-backend.azurewebsites.net/attendees', {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Accept': '*/*'
        },
        })
        .then(response => response.json())
        .then(data => {
        this.setState({campers: data.attendees});
        console.log('Success:', data.attendees);
        })
        .catch((error) => {
        console.error(error);
        });
    }

    deleteCamper(camper) {
        if (window.confirm(`Are you sure you want to delete ${camper.firstname} ${camper.lastname}`)) {
            const obj = {camper_id: camper.camper_id}
            const json = JSON.stringify(obj)
            fetch('http://localhost:5000/campers', {
                method: 'DELETE',
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
            window.location.reload()
        } else {
            console.log("Delete prevented")
        }
    }

    render() {
        return (
            <div className="GetCampers">
                <h3>Use this button to get the campers!</h3>
                <form onSubmit={this.handleSubmit}>
                    <Button type="submit" value="Submit" variant="contained">
                        Get Campers!
                    </Button>
                </form>
                {
                  this.state.campers &&
                    this.state.campers.map((camper) => 
                        <Grid>
                            <h4 key={camper.id}>{camper.firstname} {camper.lastname}</h4>
                            <Button onClick={() => {this.deleteCamper(camper)}}>Delete</Button>
                        </Grid>
                        
                    )
                }
            </div> 
        )
    }
}

export default GetCampers