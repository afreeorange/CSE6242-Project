import React from "react";
import withSizes from "react-sizes";

import Slider from "rc-slider";
import Draggable from "react-draggable";
import "rc-slider/assets/index.css";

function Timeline({ marks, onAfterChange, width, height }) {
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
      defaultPosition={{ x: 0, y: 0.83 * height - height }}
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
        />
      </div>
    </Draggable>
  );
}

const mapSizesToProps = ({ width, height }) => ({
  width: width,
  height: height,
});

export default withSizes(mapSizesToProps)(Timeline);
