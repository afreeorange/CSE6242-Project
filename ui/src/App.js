/**
 * This is the Rug that ties everything together <3
 */

import React, { useState, useEffect } from "react";

import Map from "./components/Map";
import Timeline from "./components/Timeline";
import Header from "./components/Header";
import ProjectionSwitcher from "./components/ProjectionSwitcher";
import Links from "./components/Links";
import Parameters from "./components/Parameters";

import {
  DEFAULT_PROJECTION,
  VALID_PROJECTIONS,
  SLIDER_WIDTH_IN_PX,
  DEFAULT_YEAR,
} from "./constants";

import service from "./service";

const getYear = () => {
  const d = new Date();
  return d.getFullYear();
};

const prepareTimelineMarks = data => {
  const currentYear = getYear();
  const dataWidth = Object.keys(data).length;
  const ret = {};

  Object.keys(data).map(
    (year, i) =>
      (ret[Math.round((SLIDER_WIDTH_IN_PX / dataWidth) * i)] = {
        label: year >= currentYear ? <strong>{year}</strong> : year,
        year: year,
      }),
  );

  return ret;
};

const sleep = milliseconds => {
  return new Promise(resolve => setInterval(resolve, milliseconds));
};

const App = () => {
  const [historicalData, setHistoricalData] = useState(null);
  const [year, setYear] = useState(DEFAULT_YEAR);
  const [timelineMarks, setTimelineMarks] = useState(null);
  const [projection, setProjection] = useState(DEFAULT_PROJECTION);
  const [forecastData, setForecastData] = useState(null);
  const [gdp, setGDP] = useState(0);
  const [population, setPopulation] = useState(0);

  const fetchHistoricalData = async () => {
    const _historicalData = await service.getHistoricalData();
    setHistoricalData(_historicalData);
    setTimelineMarks(prepareTimelineMarks(_historicalData));
  };

  const fetchForecastData = async (gdpDelta, populationDelta) => {
    const _forecastData = await service.getForecastData(
      gdpDelta,
      populationDelta,
    );
    setForecastData(_forecastData);
  };

  // const playOurDoom = (i) => {
  //   console.log('PLAY', i)
  //   setTimeout(function () {
  //       // Do Something Here
  //       // Then recall the parent function to
  //       // create a recursive loop.
  //       playOurDoom();
  //   }, 1000);
  // };

  const handleParameterChange = (label, value) => {
    label === "gdp" && setGDP(value);
    label === "population" && setPopulation(value);
    return true;
  };

  const handleProjectionChange = e => setProjection(e.target.value);

  const handleYearChange = timelineIndex => {
    /**
     * The component won't _always_ hand you the exact position of the slider.
     * The coordinates are usually off by 1-2 pixels. So what to do?
     * Ignore it and keep moving.
     */
    if (Object.keys(timelineMarks).indexOf(timelineIndex.toString()) === -1) {
      console.log("Skipping", timelineIndex, Object.keys(timelineMarks));
      return;
    }

    const selectedYear = timelineMarks[timelineIndex]["year"];
    setYear(selectedYear);
  };

  useEffect(() => {
    fetchHistoricalData();
  }, []);

  useEffect(() => {
    fetchForecastData(gdp, population);
  }, [gdp, population]);

  return historicalData && timelineMarks ? (
    <React.Fragment>
      <Header>
        <Links />
      </Header>
      <Map
        projection={projection}
        WSIDataForYear={
          gdp !== 0 && population !== 0 && year > getYear()
            ? forecastData[year]
            : historicalData[year]
        }
      />
      <Timeline
        marks={timelineMarks}
        defaultYearIndex={timelineMarks[year]}
        onAfterChange={handleYearChange}
      />
      <ProjectionSwitcher
        projections={VALID_PROJECTIONS}
        changeHandler={handleProjectionChange}
      />
      {year > getYear() && <Parameters changeHandler={handleParameterChange} />}
    </React.Fragment>
  ) : (
    <h1>Loading...</h1>
  );
};

export default App;
