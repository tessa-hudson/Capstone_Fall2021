import React, { Component } from 'react'
import { Button } from '@mui/material'
import '../Styles/GetGroups.css'

class GetGroups extends Component {
    constructor(props) {
        super(props)
        this.state = {groups: ''}

        this.handleSubmit = this.handleSubmit.bind(this)
    }

    handleSubmit(event) {
        event.preventDefault() //This prevents the page from refreshing on submit
        fetch('http://localhost:5000/groups', {
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
        this.setState({groups: data.groups});
        console.log('Success:', data.groups);
        })
        .catch((error) => {
        console.error(error);
        });
    }

    render() {
        return (
            <div className="GetGroup">
                <h3>Use this button to get the groups!</h3>
                <form onSubmit={this.handleSubmit}>
                    <Button type="submit" value="Submit" variant="contained">
                        Get Groups!
                    </Button>
                </form>
                {
                  this.state.groups &&
                    this.state.groups.map((group) => 
                        <h4 key={group.id}>{group.name}</h4>
                    )
                }
            </div> 
        )
    }
}

export default GetGroups