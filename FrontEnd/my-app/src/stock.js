import React, {useState} from 'react';
import StockReport from "./stockReport";
import './App.css';

function Stock(props) {
    const [stockReport, setData] = useState(null)
    const [isLoading, setIsLoading] = useState(false)

    function getReport() {
        setData(null)
        setIsLoading(true)
        fetch('http://localhost:81/report/' + props.data.Symbol)
            .then(response => response.json())
            .then(stockReport => {
                console.log(stockReport); // Do something with the response data
                setData(stockReport)// (data)
                setIsLoading(false)
            })
            .catch(error => {
                console.error('Error:', error);
                setIsLoading(false)
            });
    }

    return (
        <div>
            <div className="Stock">
            <p>{props.data.Name} ({props.data.Symbol})</p>
                <p>Trading Price: ${props.data.Price}</p>
            <button onClick={getReport}>Generate Report</button>
        </div>
            {stockReport != null? <StockReport stockReport={stockReport}></StockReport> : null}
            {isLoading ? <div className="spinner"></div> : null}
        </div>

)
    ;
}

export default Stock;
