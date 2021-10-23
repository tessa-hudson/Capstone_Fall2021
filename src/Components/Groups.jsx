import React, { Component } from 'react'
import { Box, Grid } from '@mui/material'
import AddGroupForm from './Forms/AddGroupForm'
import GetGroups from './GetGroups'

class Groups extends Component {

    render() {
        return (
            <Box sx={{flexgrow: 1}}>
                <Grid container spacing={6}>
                    <Grid item xs={12} md={6}>
                        <AddGroupForm />
                    </Grid>
                    <Grid item xs={12} md={6}>
                        <GetGroups />
                    </Grid>
                </Grid>
            </Box>   
        )
    }
}

export default Groups