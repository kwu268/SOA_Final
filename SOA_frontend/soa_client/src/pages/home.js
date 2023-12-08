import React from "react";
import { Link } from 'react-router-dom';
import './home.css'
import LoadingText from '../components/loadingText';

const Home = ({serviceInfo, loadingServices}) => {
    return (
        <div className="home-wrapper">
            <h1 className="title-text">
                Home Page 
            </h1>
            <h1 className="title-subtext">List Of Available Services</h1>
            {loadingServices && <LoadingText/>}
            <ul>
                {
                    Object.keys(serviceInfo).map((serviceName, index) => {
                        return <div key={index}>
                                    <li>
                                        <Link className="colour-link" to={`/${serviceInfo[serviceName].Name}`}>{serviceInfo[serviceName].Name}</Link>
                                        <p className="text-padding">Description: {serviceInfo[serviceName].Description}</p>
                                    </li>
                                    <br /> {/* If you need a line break between items */}
                                </div>
                    })
                }
            </ul>
        </div>
    );
};

export default Home;