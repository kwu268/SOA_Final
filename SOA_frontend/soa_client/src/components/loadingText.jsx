import React, { useState, useEffect } from 'react';

const LoadingText = () => {
  const [loadingText, setLoadingText] = useState('Loading.');

  useEffect(() => {
    const interval = setInterval(() => {
      setLoadingText(prevText => {
        const numOfPeriods = prevText.length - 7; // "Loading" is 7 characters long
        return numOfPeriods === 5 ? 'Loading.' : prevText + '.';
      });
    }, 500); // Adjust the interval as needed

    return () => clearInterval(interval);
  }, []);

  return <div>{loadingText}</div>;
};

export default LoadingText;
