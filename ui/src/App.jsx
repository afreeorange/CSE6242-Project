import React, { useState, useEffect } from "react";
import "./App.css";

import service from "./service";


const App = () => {
  const [data, setData] = useState(null);

  const fetchData = async () => {
    const sampleData = await service.getSampleData();
    setData(sampleData);
  };

  useEffect(() => {
    fetchData();
  }, []);

  return data ? (
    <React.Fragment>
    <h1>Global Water Stress Index</h1>
    <h3>{data.message}</h3>
    </React.Fragment>
  ) : (
    <h1>Loading...</h1>
  )
}

export default App;
