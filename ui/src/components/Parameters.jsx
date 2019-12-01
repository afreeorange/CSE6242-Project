import React from "react";
import withSizes from "react-sizes";
import Slider from "rc-slider";
import Draggable from "react-draggable";
import "rc-slider/assets/index.css";

const Parameters = ({ width, height }) => (
  <div className="parameters">
    <h2>Adjust</h2>
    <section>
      <h3>GDP Growth Rate</h3>
      <Slider
        min={0}
        max={40}
        marks={{
          0: "-2",
          20: "0",
          40: "+2",
        }}
        step={20}
        included={false}
        defaultValue={20}
        className="parameter-slider"
      />
    </section>
    <section>
      <h3>Pop. Growth Rate</h3>
      <Slider
        min={0}
        max={40}
        marks={{
          0: "-2",
          20: "0",
          40: "+2",
        }}
        step={20}
        included={false}
        defaultValue={20}
        className="parameter-slider"
      />
    </section>
  </div>
);

const mapSizesToProps = ({ width, height }) => ({
  width: width,
  height: height,
});

export default withSizes(mapSizesToProps)(Parameters);
