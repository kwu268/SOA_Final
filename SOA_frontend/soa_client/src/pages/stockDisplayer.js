import React, {useState, useEffect} from "react";
import SearchDropdown from "../components/searchDropdown";
import DateRangePicker from '../components/datePicker';
import { LineChart } from "@mui/x-charts/LineChart";
import LoadingText from '../components/loadingText';

import axios from "axios";

import './servicePage.css'

const useStockDisplayer = (serviceInfo) => {

    const [loadingData, setLoadingData] = useState(false);
    const [loadingResult, setLoadingResult] = useState(false);
    const [error, setError] = useState(null);

	const [selects,setSelects] = useState([]);
	const [stock,setStock] = useState("");
	const [startDate, setStartDate] = useState("");
	const [endDate, setEndDate] = useState("");
	const [returned, setReturned] = useState(null);

	//console.log(serviceinfo)
    const displayerInfo = serviceInfo.serviceInfo.datadisplayer
	//console.log(serviceInfo)

	const getSelectionOptions = () => {
		setLoadingData(true)
		const params = {
			// your parameters here
			containerName: displayerInfo.Name,
			containerPort: displayerInfo.Port,
			endpoint: displayerInfo.Endpoints.selection
		};
		axios.get('http://localhost:3001/get-selection', { params })
			.then(response => {
				const result = response.data
				setSelects(result)
				setLoadingData(false)
			})
			.catch(error => {
				console.error('Error fetching data:', error);
				setLoadingData(false)
				setError(error.message)
			});
	}

	//API request performing service with user inputs and getting the results
	const performService = () => {
		setLoadingResult(true)
		setError(null)
		const params = {
			// your parameters here
			containerName: displayerInfo.Name,
			containerPort: displayerInfo.Port,
			endpoint: displayerInfo.Endpoints.service,			
			params: `stock_symbol=${stock}&start_date=${startDate.$y}-${startDate.$M + 1}-${startDate.$D}&end_date=${endDate.$y}-${endDate.$M + 1}-${endDate.$D}`
		};
		axios.get('http://localhost:3001/get-service', { params })
			.then(response => {
				const result = response.data
				setReturned(result)
				setLoadingResult(false)
			})
			.catch(error => {
				console.error('Error fetching data:', error);
				setLoadingResult(false)
				setError(true)
			});
	}

    //useeffect for getting stuff services 
    
	const handleSelectedItems = (items) => {
		setStock(items.symbol);
	};

	const handleDateChange = (start, end) => {
		// Handle the date change here
		// console.log('Start Date:', start, 'End Date:', end);
		// You can set these dates to state or pass them to other functions as needed
		setStartDate(start);
		setEndDate(end);
	};

	useEffect(() => {
		getSelectionOptions();
		//performService();
	}, []);

	const sendService = (event) => {
		event.preventDefault()
		setReturned(null)
		if (stock && startDate && endDate) {
			performService();
		}
	}

    return (
        <div className="wrapper">
			<h1 className="service-title">
				Stock Displayer Page
			</h1>
			<p className='description'>{displayerInfo.Description}</p>
			{error && <div>An error has occurred: {error}</div>}
			{loadingData && <div>Loading data...</div>}
			{selects &&
				<form onSubmit={sendService} className="wrapper">
					<SearchDropdown data={selects} onItemSelected={handleSelectedItems}/>
					<DateRangePicker onDateChange={handleDateChange} />
					<button type='submit' className='custom-button'>
						Submit
					</button>
				</form>				
			}
			{loadingResult && <LoadingText/>}
			{returned && 
				<LineChart 
					width = {500}
					height = {300}
					series={[{ dataKey: "Closing Price", label: "Closing Price"}]}
					xAxis={[{ scaleType: "point", dataKey: "Trade Date", label: "Trade Date"}]}
					dataset = {returned}>

				</LineChart>}
        </div>
    );
};

export default useStockDisplayer;
