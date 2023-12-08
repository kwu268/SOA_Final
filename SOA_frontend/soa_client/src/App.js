//dependencies
import { React, useState, useEffect } from "react";
import axios from 'axios';
import { Button } from "@mui/material";

//components
import Navbar from "./components/Navbar";
import {
    BrowserRouter as Router,
    Routes,
    Route,
} from "react-router-dom";
import Home from "./pages/home";
import Search from "./pages/search";
import RoiCalculator from "./pages/roiCalculator";
import StockDisplayer from "./pages/stockDisplayer";
import StockRanker from "./pages/stockRanker";
import Login from "./pages/login";

//css
import './App.css';

function App() {
	const [hasLogin, setHasLogin] = useState(false);
	const [activeServices, setActiveServices] = useState({});
	const [loadingServices, setLoadingServices] = useState(false)
	// const updateLoginStatus = (loggedIn, premium) => {
	// 	setHasLogin(loggedIn);
	// 	setIsPremium(premium);
	// }
	const getServiceList = () => {
		setLoadingServices(true)
		axios.get(`http://localhost:3001/get-available-services`)
			.then(response => {
				const result = response.data
				setActiveServices(result)
				setLoadingServices(false)
			})
			.catch(error => {
				console.error('Error fetching data:', error);
				setLoadingServices(false)
			});
	}
	
	useEffect(() => {
		getServiceList();
		}, []);


	//use effect for handling login
	useEffect(() => {
		setHasLogin(localStorage.getItem("login"));
	}, []);
	
	if (hasLogin) {	
		return (
			<div>
				<Router>
					<Navbar className="parent"/>
					<Button className="logout-button" onClick={() => {
						setHasLogin(false)
					}}>logout</Button>
					<Routes>
						<Route exact path="/" element={<Home serviceInfo={activeServices} loadingServices={loadingServices}/>} />
						<Route path="/search" element={<Search  serviceInfo={activeServices} loadingServices = {loadingServices}/>} />
						<Route path="/pastyields" element={<RoiCalculator serviceInfo={activeServices}/>}/>
						<Route path="/datadisplayer" element={<StockDisplayer serviceInfo={activeServices}/>} />
						<Route path="/ranker" element={<StockRanker serviceInfo ={activeServices}/>} /> 
					</Routes>
				</Router>
			<Button className="custom-button" onClick={getServiceList}>Refresh</Button>
			</div>
		);
	}  else {
		return(
			<Login />
		);
	}
}

export default App;