import React, {Component} from 'react'
import { Button, Grid } from '@mui/material'
import { Link } from "react-router-dom"
import '../Styles/GetAttendees.css'

class GetAttendees extends Component {
    

    constructor(props) {
        super(props)
        this.state = {Attendees: []}

        this.handleSubmit = this.handleSubmit.bind(this)
        this.deleteAttendee = this.deleteAttendee.bind(this)
    }

    handleSubmit(event) {
        event.preventDefault() //This prevents the page from refreshing on submit
        fetch('https://hbda-tracking-backend.azurewebsites.net/attendees', {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Accept': '*/*',
            //'Authentication': `Bearer ${this.props.accessToken}`
        },
        })
        .then(response => response.json())
        .then(data => {
        this.setState({Attendees: data.attendees});
        console.log('Success:', data.attendees);
        })
        .catch((error) => {
        console.error(error);
        });
    }

    deleteAttendee(attendee) {
        if (window.confirm(`Are you sure you want to delete ${attendee.firstname} ${attendee.lastname}`)) {
            fetch(`https://hbda-tracking-backend.azurewebsites.net/attendees/${attendee.attendee_id}`, {
                method: 'DELETE',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Accept': '*/*'
                },
                })
                .then(response => response.json())
                .then(data => {
                console.log('Success:', data);
                })
                .catch((error) => {
                console.error(error);
                });
            setTimeout(function(){window.location.reload()}, 1000)
        } else {
            console.log("Delete prevented")
        }
    }

    render() {
        return (
            <div className="GetAttendees">
                <h3>Use this button to get the attendees!</h3>
                <form onSubmit={this.handleSubmit}>
                    <Button type="submit" value="Submit" variant="contained">
                        Get Attendees!
                    </Button>
                </form>
                {
                  this.state.Attendees &&
                    this.state.Attendees.map((attendee) => 
                        <Grid key={attendee.attendee_id}>
                            <h4>{attendee.firstname} {attendee.lastname}</h4>
                            <Button onClick={() => {this.deleteAttendee(attendee)}}>Delete</Button>
                            <Link to={{pathname:"/update", state: ['attendee', attendee]}}>
                                <Button>Update</Button>
                            </Link>
                        </Grid>
                        
                    )
                }
            </div> 
        )
    }
}

export default GetAttendees