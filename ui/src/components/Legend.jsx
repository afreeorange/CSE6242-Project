import React from "react";

import { colorScale, COLOR_SCALE_TICKS } from "../constants";

const Legend = () => (
  <div className="legend">
    <div className="legend-text">Water Stress Index</div>
    <div className="legend-items">
    {COLOR_SCALE_TICKS.map(tick => (
      <div className="legend-item">
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
