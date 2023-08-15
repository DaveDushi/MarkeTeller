import logo from './crystal_ball.jpeg';
import './App.css';
import Stock from "./stock";
import {useEffect, useState} from "react";
let data = null;

function App() {
    const [data, setData] = useState(null)
    function getStock() {
        setData((null))
        fetch('http://localhost:81/stock-pick')
          .then(response => response.json())
          .then(data => {
            console.log(data); // Do something with the response data
              setData(data)// (data)
          })
          .catch(error => {
            console.error('Error:', error);
          });
    }

  return (
    <div className="App">
      <header className="App-header">
          <h1 className="App-title">MarkeTeller</h1>
          <img src={logo} className="App-logo" alt="logo" />
        <button onClick={getStock} >Get Stock Pick</button>
      </header>
        <div className="Stock-container">
        {data != null ? <Stock data={data} /> : null}
      </div>
    </div>
  );
}

export default App;
