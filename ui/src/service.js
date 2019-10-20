import axios from "axios";

import { UPSTREAM_API } from "./constants";

class WSIService {
  getSampleData = () => axios.get(`${UPSTREAM_API}/data`).then(r => r.data);
}

/**
 * Export singleton. And call it "service" for we have no other
 * services... just the one.
 */
const service = new WSIService();
export default service;
