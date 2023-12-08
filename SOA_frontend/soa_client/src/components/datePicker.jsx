import React, { useState } from 'react';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { TextField } from '@mui/material';
import dayjs from 'dayjs';

const DateRangePicker = ({ onDateChange }) => {
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

  const handleStartDateChange = (newStartDate) => {
    setStartDate(newStartDate);
    onDateChange(newStartDate, endDate);
  };

  const handleEndDateChange = (newEndDate) => {
    setEndDate(newEndDate);
    onDateChange(startDate, newEndDate);
  };

  const shouldDisableStartDate = (date) => {
    // Disable start dates after the currently selected end date
    return endDate ? dayjs(date).isAfter(endDate) : false;
  };

  const shouldDisableEndDate = (date) => {
    // Disable end dates before the currently selected start date
    return startDate ? dayjs(date).isBefore(startDate) : false;
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <DatePicker
        label="Start Date"
        value={startDate}
        onChange={handleStartDateChange}
        renderInput={(params) => <TextField {...params} />}
        shouldDisableDate={shouldDisableStartDate}
        minDate={dayjs('2015-01-01')}
        maxDate={endDate || dayjs('2020-12-31')}
      />
      <DatePicker
        label="End Date"
        value={endDate}
        onChange={handleEndDateChange}
        renderInput={(params) => <TextField {...params} />}
        shouldDisableDate={shouldDisableEndDate}
        minDate={startDate  || dayjs('2015-01-01')}
        maxDate={dayjs('2020-12-31')}
      />
    </LocalizationProvider>
  );
};

export default DateRangePicker;
