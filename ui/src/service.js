import axios from "axios";

class WSIService {
  getGeography = () => axios.get("/countries-110m.json").then(r => r.data);

  getHistoricalData = () => axios.get(`/wsi`).then(r => r.data);

  getForecastData = (gdpDelta, populationDelta) =>
    axios
      .get(`/predict`, {
        params: {
          gdp_delta: gdpDelta,
          population_delta: populationDelta,
        },
      })
      .then(r => r.data);
}

/**
 * Export singleton. And call it "service" for we have no other
 * services... just the one.
 */
const service = new WSIService();
export default service;
