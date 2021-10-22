import React, { Component } from 'react'
import { Box, Grid } from '@mui/material'
import AddCamperForm from './Forms/AddCamperForm'
import GetCampers from './GetCampers'

class Campers extends Component {

    render() {
        return (
            <Box sx={{flexgrow: 1}}>
                <Grid container spacing={6}>
                    <Grid item xs={12} md={6}>
                        <AddCamperForm />
                    </Grid>
                    <Grid item xs={12} md={6}>
                        <GetCampers />
                    </Grid>
                </Grid>
            </Box>   
        )
    }
}

export default Campers