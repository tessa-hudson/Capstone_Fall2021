import React from 'react'
import { Box, Grid } from '@mui/material'
import AddAttendeeForm from './Forms/AddAttendeeForm'
import GetAttendees from './GetAttendees'
import {useAuth0} from "@auth0/auth0-react"

const Attendees = () => {
    // const {getAccessTokenSilently} = useAuth0()
    // const accessToken = getAccessTokenSilently()

    
        return (
            <Box sx={{flexgrow: 1}}>
                <Grid container spacing={6}>
                    <Grid item xs={12} md={6}>
                        <AddAttendeeForm /*accessToken={accessToken}*//>
                    </Grid>
                    <Grid item xs={12} md={6}>
                        <GetAttendees /*accessToken={accessToken}*//>
                    </Grid>
                </Grid>
            </Box>   
        )
}

export default Attendees