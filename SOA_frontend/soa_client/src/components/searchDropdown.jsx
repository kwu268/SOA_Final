import React, { useState } from 'react';
import Autocomplete from '@mui/material/Autocomplete';
import { TextField } from '@mui/material';

const SearchDropdown = ({ data, onItemSelected, isDisabled=false }) => {
  const [selectedItem, setSelectedItem] = useState(null);

  const handleItemSelection = (newValue) => {
    setSelectedItem(newValue);
    onItemSelected(newValue);
  };

  return (
    <div>
      <Autocomplete
        disabled = {isDisabled}
        options={data}
        getOptionLabel={(option) => `${option.companyName} (${option.symbol})`}
        style={{ width: '400px' }}
        renderInput={(params) => (
          <TextField {...params} label="Search Companies" variant="outlined" />
        )}
        onChange={(event, newValue) => {
          handleItemSelection(newValue);
        }}
        value={selectedItem}
      />
    </div>
  );
}
export default SearchDropdown;