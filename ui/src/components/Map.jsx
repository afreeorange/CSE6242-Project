import React from "react";
import {
  ComposableMap,
  Geographies,
  Geography,
  ZoomableGroup,
} from "react-simple-maps";
import { PatternLines } from "@vx/pattern";
import tooltip from "wsdm-tooltip";

import { D3_GEO_URL, colorScale } from "../constants";

import "./Map.css";

/**
 * Tooltip stuff
 */
const tooltipper = tooltip();
tooltipper.create();

const handleMouseEnter = (e, text) => {
  tooltipper.position({ pageX: e.pageX, pageY: e.pageY });
  tooltipper.show(text);
};
const handleMouseExit = e => tooltipper.hide();

/**
 * Behold the Map component
 */
const Map = ({ projection, WSIDataForYear }) => (
  <div>
    <ComposableMap projection={projection} width={980} height={800}>
      <PatternLines
        id="crosshatch"
        height={5}
        width={5}
        stroke="#ddd"
        strokeWidth={1}
        orientation={["diagonal"]}
      />
      <ZoomableGroup zoom={1}>
        <Geographies geography={D3_GEO_URL}>
          {({ geographies }) =>
            geographies.map(geo => {
              const dataAvailable =
                Object.keys(WSIDataForYear).indexOf(geo.properties.name) >= 0;

              const geoProps = {
                fill: dataAvailable
                  ? colorScale(WSIDataForYear[geo.properties.name])
                  : "url('#crosshatch')",
                tooltipText: `
                    <strong>${geo.properties.name}</strong>
                    <br />
                    <small>${
                      dataAvailable
                        ? `<strong>${
                            WSIDataForYear[geo.properties.name]
                          }</strong>`
                        : "WSI Data Unavilable"
                    }</small>
                  `,
              };

              return (
                <Geography
                  haha={geo.properties.name}
                  key={geo.rsmKey}
                  geography={geo}
                  onMouseMove={e =>
                    handleMouseEnter(e, geoProps["tooltipText"])
                  }
                  onMouseLeave={handleMouseExit}
                  className="crosshatch"
                  style={{
                    default: {
                      fill: geoProps["fill"],
                      stroke: "#ccc",
                      strokeWidth: 0.25,
                      outline: "none",
                    },
                    hover: {
                      fill: geoProps["fill"],
                      stroke: "#000",
                      strokeWidth: 0.75,
                      outline: "none",
                      cursor: "pointer",
                    },
                  }}
                />
              );
            })
          }
        </Geographies>
      </ZoomableGroup>
    </ComposableMap>
  </div>
);

export default Map;
