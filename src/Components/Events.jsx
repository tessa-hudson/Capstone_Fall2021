import React, { Component } from 'react'
import { Box, Grid } from '@mui/material'
import AddEventForm from './Forms/AddEventForm'

class Events extends Component {

    render() {
        return (
            <Box sx={{flexgrow: 1}}>
                <Grid container spacing={6}>
                    <Grid item xs={12} md={6}>
                        <AddEventForm />
                    </Grid>
                    <Grid item xs={12} md={6}>
                        <h1>temp</h1>
                    </Grid>
                </Grid>
            </Box>   
        )
    }
}

export default Events