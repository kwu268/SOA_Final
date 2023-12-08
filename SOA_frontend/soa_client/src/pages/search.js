import {React, useState} from "react";
import { Link } from 'react-router-dom';
import './search.css';
import LoadingText from '../components/loadingText';


const Search = ({serviceInfo, loadingServices}) => {
    const [searchText, setSearchText] = useState('');

    const filterServices = (text) => {
        return Object.entries(serviceInfo)
            .filter(([serviceName]) =>
            serviceName.toLowerCase().includes(text.toLowerCase())
            )
            .map(([serviceName, serviceData]) => ({
            name: serviceName,
            description: serviceData.Description,
            }));
        };

    const handleSearchChange = (event) => {
        setSearchText(event.target.value);
    };

    const filteredServices = filterServices(searchText);


    return (
        <div className="search-wrapper">
            <h1 className="service-title">
                Search page
            </h1>
            <div>
                <label>Search Services: </label>
                <input
                type="text"
                value={searchText}
                onChange={handleSearchChange}
                placeholder="Enter service name"
                className="search-input"
                />
            </div>

            <h3 className="service-title">Results</h3>
            {loadingServices && <LoadingText/>}

            {searchText && filteredServices.length > 0 && (
            <div className="results-wrapper">
                <ul className="colour-list">
                {filteredServices.map(({ name, description }) => (
                <Link to={`/${name}`} className="link">
                    {name}  <p>Description: {description}</p>
                </Link>
                ))}
                </ul>
            </div>
            )}
        </div>
    );
};

export default Search;