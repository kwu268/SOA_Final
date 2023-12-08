import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';

export default function BasicTextFields({ onItemsSelected }) {

  const handleChange = (event) => {
    // Check if onItemsSelected is a function before calling it
    if (typeof onItemsSelected === 'function') {
      onItemsSelected(event.target.value);
    }
  };

  return (
    <Box
      component="form"
      sx={{
        '& > :not(style)': { m: 1, width: '25ch' },
      }}
      noValidate
      autoComplete="off"
    >
      <TextField 
        id="outlined-basic" 
        label="Date" 
        variant="outlined"
        onChange={handleChange} // Add the onChange event handler
      />
    </Box>
  );
}