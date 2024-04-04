import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
// Import the background image
import backgroundImage from '/Users/sigurdherland/Documents/eit/eit/src/images/background.png'; // Adjust the path as needed

function App() {
  const [flightFrom, setFlightFrom] = useState('');
  const [flightTo, setFlightTo] = useState('');
  const [data, setData] = useState([]);
  const [topText, setTopText] = useState(''); // State to store the top text
  const [isFormSubmitted, setIsFormSubmitted] = useState(false); // State to track if the form has been submitted

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/flights', { flightFrom, flightTo });
      const responseData = response.data;
      if (responseData.length === 3) {
        // Assuming the first two elements are numbers for the bar chart
        setData(responseData.slice(0, 2));
        // The third element is a string for the top center text
        setTopText(responseData[2]);
        setIsFormSubmitted(true); // Update the state to indicate the form has been submitted
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div className="app" style={{ backgroundImage: `url(${backgroundImage})`, backgroundSize: 'cover', backgroundPosition: 'center' }}>
      {/* Conditionally render the top-text div only if topText is not an empty string */}
      {topText && (
        <div className="top-text">{topText}</div>
      )}
      {/* Conditional rendering based on isFormSubmitted */}
      {!isFormSubmitted && (
        <div className="form-wrapper">
          <form className="form" onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Flight From"
              value={flightFrom}
              onChange={(e) => setFlightFrom(e.target.value)}
              className="input"
            />
            <input
              type="text"
              placeholder="Flight To"
              value={flightTo}
              onChange={(e) => setFlightTo(e.target.value)}
              className="input"
            />
            <button type="submit" className="button">Submit</button>
          </form>
        </div>
      )}
     {data.length > 0 && (
      <div className="bar-chart">
        {data.map((value, index) => (
          <div key={index} className="bar-container">
            <div className="bar" style={{height: `${value*1.15}px`}}>{value.toFixed(3)} kg CO<sub>2</sub></div>
            <div className="bar-label">{index === 0 ? 'Hydrogen' : 'Conventional'}</div>
          </div>
        ))}
      </div>
    )}
    </div>
  );
}

export default App;
