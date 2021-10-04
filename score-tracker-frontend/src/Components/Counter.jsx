import React, { Component } from 'react'
import { Button } from '@mui/material'

const Counter = (props) => {
    return (
        <tr key={props.id}>
            <th>{props.name}</th>
            <th><Button variant="contained" onClick={() => props.decrement(props.id)}>-</Button></th>
            <th>{props.count}</th>
            <th><Button variant="contained" onClick={() => props.increment(props.id)}>+</Button></th>
        </tr>
    )
}

export default Counter