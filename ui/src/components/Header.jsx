import React from "react";

const Header = ({ children }) => {
  return (
    <header>
      <h1>Global Water Stress Index</h1>
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
