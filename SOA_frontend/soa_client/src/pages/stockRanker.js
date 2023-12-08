import React, { useState, useEffect } from 'react';
import SearchDropdown from '../components/searchDropdown';
import DateRangePicker from '../components/datePicker';
import LoadingText from '../components/loadingText';
import './servicePage.css'
import axios from 'axios';


const StockRanker = (serviceInfo) => {
	const [data, setData] = useState([]);
    const [loadingData, setLoadingData] = useState(false);
    const [loadingResults, setLoadingResults] = useState(false);
    const [error, setError] = useState(null);
	const [stockList, setStockList] = useState(null);
	const [selectedStock, setSelectedStock] = useState(null);
	const [startDate, setStartDate] = useState(null);
	const [endDate, setEndDate] = useState(null);

    const info = serviceInfo.serviceInfo.ranker
	const port = info.Port
	const name = info.Name
	const endpointSel = info.Endpoints.selection 
	const endpointSer = info.Endpoints.service

    const getSelections = () => { 
		setLoadingData(true)

        const params = {
            containerName: name,
            containerPort: port,
            endpoint: endpointSel
        };

        axios.get('http://localhost:3001/get-selection', { params })
        .then(response => {
            const result = response.data
			setStockList(result);
			setLoadingData(false);

        })
        .catch(error => {
			setLoadingData(false)
			setError(error.message)
            console.error('Error fetching data:', error);
        });
    }

	//API request performing service with user inputs and getting the results
	const performSerivce = () => {
		setLoadingResults(true)
		const params = {
			// your parameters here
			containerName: name,
			containerPort: port,
			endpoint: endpointSer,
			params: `stock_symbol=${selectedStock.symbol}&start_date=${startDate.$y}-${startDate.$M + 1}-${startDate.$D}&end_date=${endDate.$y}-${endDate.$M + 1}-${endDate.$D}`
		};
		axios.get('http://localhost:3001/get-service', { params })
			.then(response => {
				const result = response.data
				setLoadingResults(false);
				setData(result);
			})
			.catch(error => {
				console.error('Error fetching data:', error);
				setLoadingResults(false);
				setError(true)
			});
	}

	const handleData = (data) => {
		console.log(data.length > 0)
		if (data.length <= 0) return null;

		const [selectedStockIndex, stocks] = data;
		const myStock = stocks[selectedStockIndex];

		const rankedStocks = stocks.map((stock, index) => {
			const rankMessage = `${stock[1][0]} is number ${index + 1}`;
			return <li key={index}>{rankMessage}</li>;
		});
		return (
			<div className='text-padding'>
				{myStock && <div className="result">{`Your Selected Stock, ${myStock[1][0]} stock is number ${selectedStockIndex + 1} in the sector: ${selectedStock.sector}`}</div>}
				<ul>{rankedStocks}</ul>
				
			</div>
		);
	}

	const handleSelectedItems = (item) => {
		setSelectedStock(item);
	};

	const handleDateChange = (start, end) => {
		// Handle the date change here
		setStartDate(start)
		setEndDate(end)
	};

	const submitForm = (event) => {
		setError(null)
		setData(null)
		event.preventDefault();
		if(selectedStock != null && startDate !=null && endDate != null){
			performSerivce();
		}
	}

    useEffect(() => {
        getSelections();
    },[])

	return (
		<div className='wrapper'>
			<h1 className="service-title">
				Stock Ranker Page
			</h1>
			<p>{info.Description}</p>

			{error && <div>An error has occured: {error}</div>}

			{loadingData && <LoadingText/>}

			{stockList && 
				<form onSubmit={submitForm} className='wrapper'>
					<SearchDropdown data={stockList} onItemSelected={handleSelectedItems} />				
					<DateRangePicker onDateChange={handleDateChange}/>
					<button type='submit' className='custom-button'>
						Submit
					</button>
				</form>
			}
			{loadingResults && <LoadingText/>}

			{data && handleData(data)}
			
		</div>
	);
};

export default StockRanker;
