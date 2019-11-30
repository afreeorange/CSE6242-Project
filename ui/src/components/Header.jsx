import React from "react";
import ProjectionSwitcher from "./ProjectionSwitcher";

function Header({ children }) {
  console.log(typeof children);
  return (
    <header>
      <h1>Global Water Stress Index</h1>
      {typeof children !== "object" ? (
        children.map(child => <div className="header-section">{child}</div>)
      ) : (
        <div className="header-section">{children}</div>
      )}
    </header>
  );
}

export default Header;
