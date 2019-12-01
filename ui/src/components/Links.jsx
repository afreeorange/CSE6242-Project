import React, { useState } from "react";
import Modal from "react-modal";

const About = ({ isOpen, closeHandler }) => (
  <Modal
    isOpen={isOpen}
    overlayClassName="modal-overlay"
    ariaHideApp={false}
    className="modal"
  >
    <div className="about">
      <h1>About this project</h1>
      <p>
        This website was created as part of final project in{" "}
        <a href="https://www.omscs.gatech.edu/cse-6242-data-visual-analytics">
          CSE 6242, "Data and Visual Analytics"
        </a>{" "}
        at the Georgia Institute of Technology.
      </p>
    </div>
    <button onClick={closeHandler}>close</button>
  </Modal>
);

const Donate = ({ isOpen, closeHandler }) => (
  <Modal
    isOpen={isOpen}
    overlayClassName="modal-overlay"
    ariaHideApp={false}
    className="modal"
  >
    <div className="donate">
      <h1>Donate!</h1>
      <button onClick={closeHandler}>close</button>
    </div>
  </Modal>
);

const Links = () => {
  const [aboutIsOpen, toggleAbout] = useState(false);
  const [donateIsOpen, toggleDonate] = useState(false);

  const handleAbout = () => toggleAbout(!aboutIsOpen);
  const handleDonate = () => toggleDonate(!donateIsOpen);

  return (
    <React.Fragment>
      <nav>
        <ul>
        <li>
          <a href="#about" onClick={handleAbout}>
            About
          </a>
        </li>
        <li>
          <a href="#donate" onClick={handleDonate}>
            Donate
          </a>
        </li>
        </ul>
      </nav>

      {aboutIsOpen && <About isOpen={aboutIsOpen} closeHandler={handleAbout} />}
      {donateIsOpen && (
        <Donate isOpen={donateIsOpen} closeHandler={handleDonate} />
      )}
    </React.Fragment>
  );
};

export default Links;
