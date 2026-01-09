import './App.css';
import { useState } from 'react';
import heightConversion from './Convert-Foot-Inches-to-Centimeters.png';
import weightConversion from './Pounds-to-Kg.png';
import shoeSizeConversion from './shoesize-conversion.png';

function App() {
  const [height, setHeight] = useState('');
  const [weight, setWeight] = useState('');
  const [shoeSize, setShoeSize] = useState('');
  const [prediction, setPrediction] = useState('');
  const [confidence, setConfidence] = useState('');
  const [activeTab, setActiveTab] = useState('height'); // New state for tabs

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          height: parseFloat(height),
          weight: parseFloat(weight),
          shoeSize: parseFloat(shoeSize)
        })
      });
      
      const data = await response.json();
      setPrediction(data.prediction);
      setConfidence(data.confidence);
    } catch (error) {
      console.error('Error:', error);
      setPrediction('Error making prediction');
      setConfidence('');
    }
  };

  const handleReset = () => {
    setHeight('');
    setWeight('');
    setShoeSize('');
    setPrediction('');
    setConfidence('');
  };

  const handleAddPerson = async (gender) => {
    try {
      const response = await fetch('/api/add-person', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          height: parseFloat(height),
          weight: parseFloat(weight),
          shoeSize: parseFloat(shoeSize),
          gender: gender
        })
      });
      
      const data = await response.json();
      alert(`Added to database as ${gender}`);
      handleReset();
    } catch (error) {
      console.error('Error:', error);
      alert('Error adding person to database');
    }
  };

  return (
    <div className="App">
      {/*<Analytics/>*/}
      {/*<SpeedInsights/>*/}
      
      <header className="app-header">
        <h1>Gender Predictor</h1>
      </header>

      <div className="container">
        <div className="form-section">
          <h2>Enter Your Measurements</h2>
          <form onSubmit={handleSubmit} className="prediction-form">
            <div className="form-group">
              <label htmlFor="height">Height (cm)</label>
              <input 
                id="height"
                type="number" 
                step="0.01"
                value={height} 
                onChange={(e) => setHeight(e.target.value)}
                placeholder="Enter height in cm"
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="weight">Weight (kg)</label>
              <input 
                id="weight"
                type="number" 
                step="0.01"
                value={weight} 
                onChange={(e) => setWeight(e.target.value)}
                placeholder="Enter weight in kg"
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="shoeSize">Shoe Size (EU)</label>
              <input 
                id="shoeSize"
                type="number" 
                step="0.01"
                value={shoeSize} 
                onChange={(e) => setShoeSize(e.target.value)}
                placeholder="Enter shoe size in EU"
                required
              />
            </div>
            
            <div className="button-group">
              <button type="submit" className="btn btn-primary">Predict</button>
              <button type="button" onClick={handleReset} className="btn btn-secondary">Reset</button>
            </div>
          </form>
        </div>

        <div className="conversion-guides">
          <h2>Conversion Guides</h2>
          
          <div className="tabs">
            <button 
              className={`tab-btn ${activeTab === 'height' ? 'active' : ''}`}
              onClick={() => setActiveTab('height')}
            >
              Height
            </button>
            <button 
              className={`tab-btn ${activeTab === 'weight' ? 'active' : ''}`}
              onClick={() => setActiveTab('weight')}
            >
              Weight
            </button>
            <button 
              className={`tab-btn ${activeTab === 'shoe' ? 'active' : ''}`}
              onClick={() => setActiveTab('shoe')}
            >
              Shoe Size
            </button>
          </div>

          <div className="images-container">
            {activeTab === 'height' && (
              <div className="image-card active">
                <img 
                  src={heightConversion}
                  alt="Height conversion chart: Feet and Inches to Centimeters"
                />
              </div>
            )}
            
            {activeTab === 'weight' && (
              <div className="image-card active">
                <img 
                  src={weightConversion}
                  alt="Weight conversion chart: Pounds to Kilograms"
                />
              </div>
            )}
            
            {activeTab === 'shoe' && (
              <div className="image-card active">
                <img 
                  src={shoeSizeConversion}
                  alt="Shoe size conversion chart"
                />
              </div>
            )}
          </div>
        </div>
      </div>
      
      {prediction && (
        <div className="results-section">
          <div className="results-card">
            <h2>Prediction Results</h2>
            <div className="result-item">
              <span className="label">Predicted Gender:</span>
              <span className={`prediction ${prediction.toLowerCase()}`}>
                {prediction.toUpperCase()}
              </span>
            </div>
            <div className="result-item">
              <span className="label">Confidence Score:</span>
              <span className="confidence-score">
                {(confidence * 100).toFixed(2)}%
              </span>
            </div>
            
            <div className="feedback-section">
              <h3>Was this prediction correct?</h3>
              <p>Help us improve by providing feedback:</p>
              <div className="feedback-buttons">
                <button 
                  onClick={() => handleAddPerson('male')} 
                  className="btn btn-male"
                >
                  Male
                </button>
                <button 
                  onClick={() => handleAddPerson('female')} 
                  className="btn btn-female"
                >
                  Female
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
