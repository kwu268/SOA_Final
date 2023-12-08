import React, { useState } from 'react';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';

const SingleSearchDropdown = ({ data, onItemsSelected}) => {
  const [selectedItems, setSelectedItems] = useState([]);

  const handleAddItem = (item) => {
    if (!selectedItems.some(selectedItem => selectedItem.symbol === item.symbol)) {
      const newSelectedItems = item;
      setSelectedItems(newSelectedItems);
      onItemsSelected(newSelectedItems);
    }
  };

  return (
    <div>
      <Autocomplete
        options={data}
        getOptionLabel={(option) => `${option.companyName} (${option.symbol})`}
        style={{ width: '400px' }}
        renderInput={(params) => (
          <TextField {...params} label="Search Companies" variant="outlined" />
        )}
        onChange={(event, newValue) => {
          if (newValue) {
            handleAddItem(newValue);
          }
        }}
      />
    </div>
  );
};

export default SingleSearchDropdown;