import React, { Component } from 'react'
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
        console.log(`Group Name: ${this.state.groupName}`)
    }

    render() {
        return (
            <div className="AddGroup">
                <h3>Use this form to add a new group!</h3>
                <form onSubmit={this.handleSubmit}>
                    <label>
                        Group Name:
                        <br />
                        <input type="text" value={this.state.groupName} onChange={this.handleChange} />
                    </label>
                    <br />
                    <input type="submit" value="Submit" />
                </form>
            </div>
        )
    }
}

export default AddGroupForm