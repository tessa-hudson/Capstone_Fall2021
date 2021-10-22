import React, { Component } from 'react'
import { Button } from '@mui/material'
import Counter from './Counter'
import '../Styles/Scoreboard.css'

class Scoreboard extends Component {
    constructor(props) {
        super(props)
        this.state = {groups: '', counters: []}

        this.handleSubmit = this.handleSubmit.bind(this);
        this.valueChanger = this.valueChanger.bind(this);
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

    valueChanger = (index, inc) => {
        this.setState((prevState) => {
           const counters = this.state.counters.slice();
           counters[index] += inc; 
           return {
               counters: counters
           }
        });
     }
   

    increment=(index)=>{
        this.valueChanger(index, 1);
    }
   
    decrement=(index)=>{
        this.valueChanger(index, -1);
    }

    render() {
        return (
            <div className="GetGroup">
                <h3>ScoreBoard!</h3>
                <form onSubmit={this.handleSubmit}>
                    <Button type="submit" value="Submit" variant="contained">
                        Get Groups!
                    </Button>
                </form>
                <table>
                    <tbody>
                    {
                    this.state.groups &&
                        this.state.groups.map((group) => 
                            <Counter key={group.id} name={group.name} id={group.id} decrement={this.decrement} increment={this.increment} count={0}/>
                        )
                    }
                    </tbody>
                </table>
            </div> 
        )
    }
}

export default Scoreboard;

  
  