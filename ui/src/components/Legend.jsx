import React from "react";

import { colorScale, COLOR_SCALE_TICKS } from "../constants";

import './Legend.css';

const Legend = () => (
  <div className="legend">
    <div className="legend-text">Water Stress Index</div>
    <div className="legend-items">
    {COLOR_SCALE_TICKS.map((tick, i) => (
      <div className="legend-item" key={`legend-item-${i}`}>
        <div
          className="legend-color"
          style={{ backgroundColor: colorScale(tick) }}
        />
        <div className="legend-label">{tick}</div>
      </div>
    ))}
    </div>
  </div>
);

export default Legend;
