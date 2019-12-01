import React from "react";

const ProjectionSwitcher = ({ projections, changeHandler }) => (
  <div className="projection-switcher">
    <span className="projection-label">Projection</span>
    <select onChange={changeHandler}>
      {Object.keys(projections).map(projectionName => (
        <option value={projections[projectionName]}>{projectionName}</option>
      ))}
    </select>
  </div>
);

export default ProjectionSwitcher;
