import React from "react";
import { IoIosWater } from "react-icons/io";

import './Header.css';

const Header = ({ children }) => {
  return (
    <header>
      <h1>
        <IoIosWater className="icon-water" /> Global{" "}
        <strong>Water Stress Index</strong>
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
