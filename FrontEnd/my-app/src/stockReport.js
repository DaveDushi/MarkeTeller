import React, {useState} from 'react';
import './App.css';

function StockReport(props) {
  const sections = props.stockReport.Report.split('\n\n');

  return (
    <div className="StockReport">
      {sections.map((section, index) => (
        <React.Fragment key={index}>
          <p>{section}</p>
        </React.Fragment>
      ))}
    </div>
  );
}

export default StockReport;
