import React, { Component } from 'react'
import { Button, Grid } from '@mui/material'
//import { Popover, Typograghy } from '@mui/material'
//import PopupState, { bindTrigger, bindPopover } from 'material-ui-popup-state';
import { Link } from "react-router-dom"
//import { default as ReactSelect } from "react-select";
//import { components } from "react-select";
import '../Styles/GetGroups.css'

// const Option = (props) => {
//     return (
//       <div>
//         <components.Option {...props}>
//           <input
//             type="checkbox"
//             checked={props.isSelected}
//             onChange={() => null}
//           />{" "}
//           <label>{props.label}</label>
//         </components.Option>
//       </div>
//     );
// };

class GetGroups extends Component {
    constructor(props) {
        super(props)
        this.state = {groups: []}

        this.handleSubmit = this.handleSubmit.bind(this)
        this.handleGroupSubmit = this.handleGroupSubmit.bind(this)
        this.handleChange = this.handleChange.bind(this)
        this.getCampers = this.getCampers.bind(this)
        this.getoptions = this.getOptions.bind(this)
        this.deleteGroup = this.deleteGroup.bind(this)
    }

    handleSubmit(event) {
        event.preventDefault() //This prevents the page from refreshing on submit
        fetch('https://hbda-tracking-backend.azurewebsites.net/groups', {
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

    deleteGroup(group) {
        if (window.confirm(`Are you sure you want to delete ${group.group_name}`)) {
            fetch(`https://hbda-tracking-backend.azurewebsites.net/groups/${group.group_id}`, {
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
            window.location.reload()
        } else {
            console.log("Delete prevented")
        }
    }

    handleChange = (selected) => {
        this.setState({
          optionSelected: selected
        });
    };

    getCampers() {
        fetch('http://localhost:5000/attendees', {
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
            //console.log('Success:', data.attendees);
            })
            .catch((error) => {
            console.error(error);
            });
    }

    getOptions() {
        //this.getCampers
        let campers = this.state.campers
        let options = []
        for (var i=0; i<campers.length; i++) {
            options.push({value: campers[i].firstname + ' ' + campers[i].last_initial, label: campers[i].firstname + ' ' + campers[i].last_initial, id: campers[i].id})
        }
        return options
    }

    handleGroupSubmit(event) {
        event.preventDefault() //This prevents the page from refreshing on submit
        //const obj = {name: this.state.eventName, type: this.state.eventType, startDate: startDate, endDate: endDate}
        let ids = []
        for (var i=0; i<this.state.optionSelected.length; i++) {
            ids.push(this.state.optionSelected[i].id)
        }
        //const json = JSON.stringify(obj);
        console.log( {attendees: ids} )
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
                        <Grid key={group.group_id}>
                            <h4>{group.group_name}</h4>
                            <Button onClick={() => {this.deleteGroup(group)}}>Delete</Button>
                            <Link to={{pathname:"/update", state: ['group', group]}}>
                                <Button>Update</Button>
                            </Link>
                        </Grid>
                    )
                }
            </div> 
        )
    }
}

export default GetGroups

// import React, { Component } from 'react'
// import { Button, Grid, Popover, Typography } from '@mui/material'
// import PopupState, { bindTrigger, bindPopover } from 'material-ui-popup-state';
// import { default as ReactSelect } from "react-select";
// import { components } from "react-select";
// import '../Styles/GetGroups.css'

// const Option = (props) => {
//     return (
//       <div>
//         <components.Option {...props}>
//           <input
//             type="checkbox"
//             checked={props.isSelected}
//             onChange={() => null}
//           />{" "}
//           <label>{props.label}</label>
//         </components.Option>
//       </div>
//     );
// };

// class GetGroups extends Component {
//     constructor(props) {
//         super(props)
//         this.state = {groups: '', optionSelected: null, campers: []}

//         this.handleSubmit = this.handleSubmit.bind(this)
//         this.handleGroupSubmit = this.handleGroupSubmit.bind(this)
//         this.handleChange = this.handleChange.bind(this)
//         this.getCampers = this.getCampers.bind(this)
//         this.getoptions = this.getOptions.bind(this)
//     }

//     handleSubmit(event) {
//         event.preventDefault() //This prevents the page from refreshing on submit
//         fetch('http://localhost:5000/groups', {
//         method: 'GET',
//         mode: 'cors',
//         headers: {
//             'Content-Type': 'application/json',
//             'Access-Control-Allow-Origin': '*',
//             'Accept': '*/*'
//         },
//         })
//         .then(response => response.json())
//         .then(data => {
//         this.setState({groups: data.groups});
//         console.log('Success:', data.groups);
//         })
//         .catch((error) => {
//         console.error(error);
//         });
//     }

//     handleChange = (selected) => {
//         this.setState({
//           optionSelected: selected
//         });
//     };

//     getCampers() {
//         fetch('http://localhost:5000/attendees', {
//             method: 'GET',
//             mode: 'cors',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'Access-Control-Allow-Origin': '*',
//                 'Accept': '*/*'
//             },
//             })
//             .then(response => response.json())
//             .then(data => {
//             this.setState({campers: data.attendees});
//             //console.log('Success:', data.attendees);
//             })
//             .catch((error) => {
//             console.error(error);
//             });
//     }

//     getOptions() {
//         //this.getCampers
//         let campers = this.state.campers
//         let options = []
//         for (var i=0; i<campers.length; i++) {
//             options.push({value: campers[i].firstname + ' ' + campers[i].last_initial, label: campers[i].firstname + ' ' + campers[i].last_initial, id: campers[i].id})
//         }
//         return options
//     }

//     handleGroupSubmit(event) {
//         event.preventDefault() //This prevents the page from refreshing on submit
//         //const obj = {name: this.state.eventName, type: this.state.eventType, startDate: startDate, endDate: endDate}
//         let ids = []
//         for (var i=0; i<this.state.optionSelected.length; i++) {
//             ids.push(this.state.optionSelected[i].id)
//         }
//         //const json = JSON.stringify(obj);
//         console.log( {attendees: ids} )
//     }

//     render() {
//         return (
//             <div className="GetGroup">
//                 <h3>Use this button to get the groups!</h3>
//                 <form onSubmit={this.handleSubmit}>
//                     <Button type="submit" value="Submit" variant="contained" onClick={this.getCampers}>
//                         Get Groups!
//                     </Button>
//                 </form>
//                 {
//                   this.state.groups &&
//                     this.state.groups.map((group) => 
//                     <Grid key={group.id}>
//                         <Grid item>
//                             <h4>{group.name}</h4>
//                         </Grid>
//                         <Grid item>
//                             <PopupState variant="popover" popupId="demo-popup-popover">
//                                 {(popupState) => (
//                                     <div>
//                                     <Button variant="contained" {...bindTrigger(popupState)}>
//                                         Add Campers
//                                     </Button>
//                                     <Popover
//                                         {...bindPopover(popupState)}
//                                         anchorOrigin={{
//                                             vertical: 'bottom',
//                                             horizontal: 'center',
//                                         }}
//                                         transformOrigin={{
//                                             vertical: 'top',
//                                             horizontal: 'center',
//                                         }}
//                                     >
//                                         <div className={"SelectForm"}>
//                                             <Typography sx={{ p: 2 }}>{group.name}</Typography>
//                                             <form onSubmit={this.handleGroupSubmit}>
//                                                 <ReactSelect
//                                                     options={this.getOptions()}
//                                                     isMulti
//                                                     closeMenuOnSelect={false}
//                                                     hideSelectedOptions={false}
//                                                     components={{
//                                                         Option
//                                                     }}
//                                                     onChange={this.handleChange}
//                                                     allowSelectAll={false}
//                                                     value={this.state.optionSelected}
//                                                 />
//                                                 <Button type="submit" value="Submit" variant="contained">Submit</Button>
//                                             </form>
//                                         </div>
//                                     </Popover>
//                                     </div>
//                                 )}
//                             </PopupState>
//                         </Grid>
//                     </Grid>

//                     )
//                 }
//             </div> 
//         )
//     }
// }

// export default GetGroups