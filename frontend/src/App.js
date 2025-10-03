import './App.css';
import { useState } from 'react';

function App() {
  const [height, setHeight] = useState('');
  const [weight, setWeight] = useState('');
  const [shoeSize, setShoeSize] = useState('');
  const [prediction, setPrediction] = useState('');
  const [confidence, setConfidence] = useState('');

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
      <header>
        <h2>Let's Predict Your Gender</h2>
      </header>
      
      <form onSubmit={handleSubmit}>
        <div>
          <label>Height: </label>
          <input 
            type="number" 
            step="0.01"
            value={height} 
            onChange={(e) => setHeight(e.target.value)}
            placeholder="Enter height(cm):"
          />
        </div>
        
        <div>
          <label>Weight: </label>
          <input 
            type="number" 
            step="0.01"
            value={weight} 
            onChange={(e) => setWeight(e.target.value)}
            placeholder="Enter weight(kg)"
          />
        </div>
        
        <div>
          <label>Shoe Size: </label>
          <input 
            type="number" 
            step="0.01"
            value={shoeSize} 
            onChange={(e) => setShoeSize(e.target.value)}
            placeholder="Enter shoe size(EU)"
          />
        </div>
        
        <div>
          <button type="submit">Submit</button>
          <button type="button" onClick={handleReset}>Reset</button>
        </div>
      </form>
      
      {prediction && (
        <div>
          <h3>Results:</h3>
          <p>Prediction: {prediction}</p>
          <p>Confidence: {confidence}</p>
          
          <div>
            <h3>What's Your Actual Gender:</h3>
            <button onClick={() => handleAddPerson('male')}>Male</button>
            <button onClick={() => handleAddPerson('female')}>Female</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
