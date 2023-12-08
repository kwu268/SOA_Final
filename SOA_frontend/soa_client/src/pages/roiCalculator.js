import React, { useState, useEffect } from 'react';
import SingleSearchDropdown from '../components/singleSearchDropdown';
import SearchDropdown from '../components/searchDropdown';

import DateRangePicker from '../components/datePicker';
import LoadingText from '../components/loadingText';

import axios from 'axios';
import './servicePage.css'



const RoiCalculator = (serviceinfo) => {

    const [roi, setRoi] = useState([]);
    const [loadingData, setLoadingData] = useState(false);
	const [loadingRoi, setLoadingRoi] = useState(false);
    const [error, setError] = useState(false);
	const [stockList, setStockList] = useState(null);
	const [selectedStocks, setSelectedStocks] = useState(null);
	const [startDate, setStartDate] = useState(null);
	const [endDate, setEndDate] = useState(null);

	// console.log(serviceinfo.serviceInfo.pastyields)

	const roiInfo = serviceinfo.serviceInfo.pastyields
	const port = roiInfo.Port
	const name = roiInfo.Name
	const endpoint = roiInfo.Endpoints.selection   
	const service = roiInfo.Endpoints.service

    //API request to return selection options for inputs of a specific service
	const getSelectionOptions = () => {
		setLoadingData(true);
		const params = {
			// your parameters here
			containerName: name,
			containerPort: port,
			endpoint: endpoint,
		};
		axios.get('http://localhost:3001/get-selection', { params })
			.then(response => {
				const result = response.data
				setStockList(result)
				setLoadingData(false);
			})
			.catch(error => {
				setLoadingData(false)
				setError(error.message)
				console.error('Error fetching data:', error);
			});
	}

	//API request performing service with user inputs and getting the results
	const performService = () => {
		setLoadingRoi(true)
		const params = {
			// your parameters here
			containerName: name,
			containerPort: port,
			endpoint: service,
			params: `stock_symbol=${selectedStocks.symbol}&start_date=${startDate.$y}-${startDate.$M+1}-${startDate.$D}&end_date=${endDate.$y}-${endDate.$M+1}-${endDate.$D}`
		};
		axios.get('http://localhost:3001/get-service', { params })
			.then(response => {
				const result = response.data
				setRoi(result.yield_percent.toFixed(2));
				setLoadingRoi(false)
			})
			.catch(error => {
				setLoadingRoi(false)
				setError(error.message)
				console.error('Error fetching data:', error);
			});
	}


	const handleSelectedItems = (items) => {
		setSelectedStocks(items);
	};

	const handleDateChange = (start, end) => {
		// Handle the date change here
		setStartDate(start);
		setEndDate(end);
		// You can set these dates to state or pass them to other functions as needed
	};

	const submitService = (event) => {
		event.preventDefault();
		setRoi(null)
		setError(null)
		if(endDate && startDate && selectedStocks){
			performService()
		}
		// console.log(event.target);
	}


    //useeffect for getting stuff services 
    
	useEffect(() => {
        getSelectionOptions();
		}, []);

     // Empty dependency array ensures this effect runs only once

    return (
        <div className='wrapper'>
			<h1 className="service-title">
				Roi Calculator Page
			</h1>
			<p className='description'>{roiInfo.Description}</p>
			{error && <div>An error has occurred: {error}</div>}
			{loadingData && <div><LoadingText/></div>}
            {stockList && 
				<form onSubmit={submitService} className='wrapper'>
					<SearchDropdown className="test" data={stockList} onItemSelected={handleSelectedItems} />
					<DateRangePicker onDateChange={handleDateChange} />
					<button type='submit' className='custom-button'>
						Submit
					</button>
				</form> }

            <h1 className='row'>ROI Result (%): 
				{loadingRoi && 
					<div><LoadingText/></div>} 
				{roi && 
					<div>&nbsp;{roi}</div>}
			</h1>
	

        </div>
        
    );
};

export default RoiCalculator;