import React from 'react'
import { Box, Grid } from '@mui/material'
import AddAttendeeForm from './Forms/AddAttendeeForm'
import GetAttendees from './GetAttendees'

const Attendees = () => {
    
        return (
            <Box sx={{flexgrow: 1}}>
                <Grid container spacing={6}>
                    <Grid item xs={12} md={6}>
                        <AddAttendeeForm />
                    </Grid>
                    <Grid item xs={12} md={6}>
                        <GetAttendees />
                    </Grid>
                </Grid>
            </Box>   
        )
}

export default Attendees