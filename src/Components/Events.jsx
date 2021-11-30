import React, { Component } from 'react'
import { Box, Grid } from '@mui/material'
import AddEventForm from './Forms/AddEventForm'
import GetEvents from './GetEvents'

class Events extends Component {

    render() {
        return (
            <Box sx={{flexgrow: 1}} style={{maxWidth:'80%', margin:'0 auto'}}>
                <Grid container spacing={6}>
                    <Grid item xs={12} md={6}>
                        <AddEventForm />
                    </Grid>
                    <Grid item xs={12} md={6}>
                        <GetEvents />
                    </Grid>
                </Grid>
            </Box>   
        )
    }
}

export default Events