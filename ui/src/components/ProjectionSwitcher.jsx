import React from "react";
import { FiGlobe } from "react-icons/fi";

import "./ProjectionSwitcher.css";

const ProjectionSwitcher = ({ projections, changeHandler }) => (
  <div className="projection-switcher">
    <span>
      <FiGlobe /> Projection
    </span>
    <select onChange={changeHandler}>
      {Object.keys(projections).map((i, projectionName) => (
        <option
          key={`projection-switcher-option-${i}`}
          value={projections[projectionName]}
        >
          {projectionName}
        </option>
      ))}
    </select>
  </div>
);

export default ProjectionSwitcher;
