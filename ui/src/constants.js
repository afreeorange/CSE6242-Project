import { scaleLinear } from "d3-scale";

export const VALID_PROJECTIONS = {
  Mercator: "geoMercator",
  "Mercator - Transverse": "geoTransverseMercator",
  "Conic Conformal": "geoConicConformal",
  "Conic Equal Area": "geoConicEqualArea",
  "Conic Equidistant": "geoConicEquidistant",

  /** These require rotation which I don't plan on implementing now... */
  // Albers: "geoAlbers",
  // "Azimuthal Equal Area": "geoAzimuthalEqualArea",
  // "Azimuthal Equidistant": "geoAzimuthalEquidistant",
  // Orthographic: "geoOrthographic",
};

export const DEFAULT_PROJECTION = "geoMercator";
export const DEFAULT_YEAR = 1980;
export const SLIDER_WIDTH_IN_PX = 1000;

export const D3_GEO_URL = "/countries-110m.json";
export const D3_DOMAIN = [0.1, 2, 200];
export const D3_RANGE = ["#2c7bb6", "#ffffbf", "#ca0020"];

// Doesn't really belong here but oh well...
export const colorScale = scaleLinear()
  .domain(D3_DOMAIN)
  .range(D3_RANGE);

// Legend
export const COLOR_SCALE_TICKS = [0.1, 0.5, 1, 2, 10, 50, 100, 200, 300];
