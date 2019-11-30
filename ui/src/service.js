import axios from "axios";

class WSIService {
  getWSIData = () => axios.get(`/wsi`).then(r => r.data);

  getGeography = () => axios.get('/countries-110m.json').then(r => r.data);
}

/**
 * Export singleton. And call it "service" for we have no other
 * services... just the one.
 */
const service = new WSIService();
export default service;
