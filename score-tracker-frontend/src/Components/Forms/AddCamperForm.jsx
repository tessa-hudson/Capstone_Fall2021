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
        const obj = {first: this.state.firstName, last: this.state.lastNameInitial}
        const json = JSON.stringify(obj);
        console.log(json);
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