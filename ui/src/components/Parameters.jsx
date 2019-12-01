import React from "react";
import Slider from "rc-slider";
import { MdPeopleOutline } from "react-icons/md";
import { AiOutlineDollar } from "react-icons/ai";
import "rc-slider/assets/index.css";

import './Parameters.css';

// Same ranges for sliders so use just one map :)
const marks = {
  0: "-2",
  20: "0",
  40: "+2",
};

const Parameters = ({ changeHandler }) => (
  <div className="parameters">
    <h2>Adjust</h2>
    <section>
      <h3><AiOutlineDollar />{' '}GDP Growth Rate</h3>
      <Slider
        min={0}
        max={40}
        marks={marks}
        step={20}
        included={false}
        defaultValue={20}
        onAfterChange={(e) => changeHandler("gdp", marks[e])}
        className="parameter-slider"
      />
    </section>
    <section>
      <h3><MdPeopleOutline />{' '}Pop. Growth Rate</h3>
      <Slider
        min={0}
        max={40}
        marks={marks}
        step={20}
        included={false}
        defaultValue={20}
        onAfterChange={(e) => changeHandler("population", marks[e])}
        className="parameter-slider"
      />
    </section>
  </div>
);

export default Parameters;
