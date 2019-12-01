import React from "react";
import { IoIosWater } from "react-icons/io";

import "./Header.css";

const Header = ({ year, replayIsHappening, children }) => {
  return (
    <header>
      <h1>
        <strong className={replayIsHappening ? "mild-header" : null}>
          <IoIosWater className="icon-water" />{' '}
          Global Water Stress Index
        </strong>
        {year && <span> in {year}</span>}
      </h1>
      {children &&
        (typeof children !== "object" ? (
          children.map(child => <div className="header-section">{child}</div>)
        ) : (
          <div className="header-section">{children}</div>
        ))}
    </header>
  );
};

export default Header;
