import * as React from 'react';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

export default function ComboBox(props) {

  const options = props.data ? props.data.map(company => ({
    label: company.companyName, // Displayed in the Autocomplete
    value: company.symbol       // Value when an option is selected
  })) : [];

  return (
    <Autocomplete
      disablePortal
      id="combo-box-demo"
      options={options}
      sx={{ width: 300 }}
      getOptionLabel={(option) => option.label}
      renderInput={(params) => <TextField {...params} label="Company" />}
    />
  );
}
