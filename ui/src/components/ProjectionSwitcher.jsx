import React from "react";

const ProjectionSwitcher = ({ projections, changeHandler }) => (
  <select onChange={changeHandler}>
    {Object.keys(projections).map(projectionName => (
      <option value={projections[projectionName]}>{projectionName}</option>
    ))}
  </select>
);

export default ProjectionSwitcher;
