import React, { useState } from "react";
import Draggable from "react-draggable";
import { FiMove, FiPlayCircle } from "react-icons/fi";
import Slider from "rc-slider";
import useViewportSizes from "use-viewport-sizes";
import "rc-slider/assets/index.css";

import Legend from "./Legend";

import "./Timeline.css";

const Timeline = ({ marks, onAfterChange, yearIndex, yearPlayerCallback }) => {
  const [viewportWidth, viewportHeight] = useViewportSizes();

  /**
   * This is lazy, will throw a warning but It Works(tm),
   * it's crunch time, and I don't care <3
   */
  const keys = Object.keys(marks);
  const max = keys.slice(-1)[0];
  const step = keys[1] - keys[0];

  return (
    <Draggable
      handle=".timeline"
      positionOffset={{ x: 0, y: -0.7 * viewportWidth }}
      scale={1}
      axis="y"
    >
      <div className="timeline">
        <div className="timeline-slider-wrapper">
          <FiPlayCircle
            className="timeline-play"
            onClick={yearPlayerCallback}
          />
          <Slider
            className="timeline-slider"
            min={0}
            max={parseInt(max)}
            marks={marks}
            step={parseInt(step)}
            onChange={onAfterChange}
            included={false}
            value={yearIndex}
          />
        </div>
        <Legend />
        <FiMove className="timeline-is-draggable" />
      </div>
    </Draggable>
  );
};

export default Timeline;
