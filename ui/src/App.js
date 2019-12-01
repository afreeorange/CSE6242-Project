import React, { useState, useEffect } from "react";

import Map from "./components/Map";
import Timeline from "./components/Timeline";
import Header from "./components/Header";
import ProjectionSwitcher from "./components/ProjectionSwitcher";
import Links from "./components/Links";

import {
  DEFAULT_PROJECTION,
  VALID_PROJECTIONS,
  SLIDER_WIDTH_IN_PX,
  DEFAULT_YEAR,
} from "./constants";

import service from "./service";

const prepareTimelineMarks = data => {
  const d = new Date();
  const currentYear = d.getFullYear();
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
  const [data, setData] = useState(null);
  const [year, setYear] = useState(DEFAULT_YEAR);
  const [timelineMarks, setTimelineMarks] = useState(null);
  const [projection, setProjection] = useState(DEFAULT_PROJECTION);

  const fetchData = async () => {
    const data = await service.getWSIData();
    setData(data);
    setTimelineMarks(prepareTimelineMarks(data));
  };

  const playOurDoom = (i) => {
    console.log('PLAY', i)
    setTimeout(function () {
        // Do Something Here
        // Then recall the parent function to
        // create a recursive loop.
        playOurDoom();
    }, 1000);
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

    setYear(timelineMarks[timelineIndex]["year"]);
  };

  useEffect(() => {
    fetchData();
  }, []);

  return data && timelineMarks ? (
    <React.Fragment>
      <Header>
        <Links />
      </Header>
      <Map projection={projection} WSIDataForYear={data[year]} />
      <Timeline
        marks={timelineMarks}
        defaultYearIndex={timelineMarks[year]}
        onAfterChange={handleYearChange}
      />
      <ProjectionSwitcher
          projections={VALID_PROJECTIONS}
          changeHandler={handleProjectionChange}
        />
    </React.Fragment>
  ) : (
    <h1>Loading...</h1>
  );
};

export default App;
