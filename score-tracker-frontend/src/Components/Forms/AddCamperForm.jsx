import React, { Component } from 'react'
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
        const obj = {firstname: this.state.firstName, last_initial: this.state.lastNameInitial}
        const json = JSON.stringify(obj);
        console.log(json);

        fetch('http://localhost:5000/attendees', {
        method: 'POST',
        mode: 'cors',
        cache:'no-cache',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Accept': '*/*'
        },
        body: JSON.stringify(json),
        })
        .then(response => console.log(response))
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
                    <label>
                        First Name:
                        <br />
                        <input type="text" name="firstName" value={this.state.firstName} onChange={this.handleChange} />
                    </label>
                    <br />
                    <label>
                        First Initial of Last Name:
                        <br />
                        <input type="text" name="lastNameInitial" value={this.state.lastNameInitial} onChange={this.handleChange} />
                    </label>
                    <br />
                    <input type="submit" value="Submit" />
                </form>
            </div>
        )
    }
}

export default AddCamperForm