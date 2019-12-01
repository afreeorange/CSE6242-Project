import React from "react";
import { IoIosWater } from "react-icons/io";

const Header = ({ children }) => {
  return (
    <header>
      <h1>
        <IoIosWater className="icon-water" /> Global Water Stress Index
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
