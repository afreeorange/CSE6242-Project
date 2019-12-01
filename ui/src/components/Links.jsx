import React, { useState } from "react";
import { IoMdInformationCircleOutline, IoMdClose } from "react-icons/io";
import { FaHandHoldingUsd } from "react-icons/fa";
import Modal from "react-modal";

import "./Links.css";

const GenericModal = ({ children, isOpen, closeHandler }) => {
  return (
    <Modal
      isOpen={isOpen}
      overlayClassName="modal-overlay"
      ariaHideApp={false}
      className="modal"
      onRequestClose={closeHandler}
    >
      {children}
      <IoMdClose className="close-modal" onClick={closeHandler} />
    </Modal>
  );
};

const AboutContent = () => (
  <React.Fragment>
    <h1>
      <IoMdInformationCircleOutline className="nav-icon" /> About this project
    </h1>
    <p>
      This application was created as part of final project in{" "}
      <a href="https://www.omscs.gatech.edu/cse-6242-data-visual-analytics">
        CSE 6242, "Data and Visual Analytics"
      </a>{" "}
      at the Georgia Institute of Technology. It shows historical and predicted{" "}
      <strong>Water Stress Index (WSI)</strong> which is defined as
    </p>
    <p>
      <img src="/equation.jpg" alt="Water Stress Index Equation" />
    </p>
    <p>
      It employs{" "}
      <a href="http://www.fao.org/nr/water/aquastat/data/query/">
        AQUASTAT Data
      </a>{" "}
      by the Food and Agriculture Organization of the United Nations to display
      historical WSI. It also presents forecasts, up to the year 2030 and in
      5-year increments, which may be adjusted to account for GDP and Population
      growth rates.
    </p>
    <p>
      This is a free and open-source project. See{" "}
      <a href="https://github.com/afreeorange/CSE6242-Project">
        this repository on GitHub
      </a>{" "}
      for more information on our methodology, code, and deployment.
    </p>
  </React.Fragment>
);

const DonateContent = () => (
  <React.Fragment>
    <h1>
      <FaHandHoldingUsd className="nav-icon" /> Donate!
    </h1>
    <p>
      If you've found this resource useful, consider{" "}
      <a href="https://water.org/donate/">making a gift of water</a>.
    </p>
    <p>We are not affiliated with Water.org</p>
  </React.Fragment>
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
            <a href="#" onClick={handleAbout}>
              <IoMdInformationCircleOutline className="nav-icon" /> About
            </a>
          </li>
          <li>
            <a href="#" onClick={handleDonate}>
              <FaHandHoldingUsd className="nav-icon" /> Donate
            </a>
          </li>
        </ul>
      </nav>

      {aboutIsOpen && (
        <GenericModal isOpen={aboutIsOpen} closeHandler={handleAbout}>
          <AboutContent />
        </GenericModal>
      )}
      {donateIsOpen && (
        <GenericModal isOpen={donateIsOpen} closeHandler={handleDonate}>
          <DonateContent />
        </GenericModal>
      )}
    </React.Fragment>
  );
};

export default Links;
