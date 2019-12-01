import React from "react";
import Draggable from "react-draggable";
import { FiMove } from "react-icons/fi";
import Slider from "rc-slider";
import useViewportSizes from "use-viewport-sizes";
import "rc-slider/assets/index.css";

import Legend from "./Legend";

import './Timeline.css';

const Timeline = ({
  marks,
  onAfterChange,
  defaultYearIndex,
  width,
  height,
}) => {
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
        <Slider
          min={0}
          max={parseInt(max)}
          marks={marks}
          step={parseInt(step)}
          onAfterChange={onAfterChange}
          included={false}
          defaultValue={defaultYearIndex}
        />
        <Legend />
        <FiMove className="timeline-is-draggable" />
      </div>
    </Draggable>
  );
};

export default Timeline;
