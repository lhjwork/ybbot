import axios from "axios";
import { BASE_URL } from "./url";
export const api = axios.create({
  baseURL: BASE_URL,
  // withCredentials: true,

  headers: { "Content-Type": "application/json" },
});
export const apiFormData = axios.create({
  baseURL: BASE_URL,
  // withCredentials: true,

  headers: { "Content-Type": "multipart/form-data" },
});
// api.defaults.headers.common['Authorization'] =
//     '8ac7b4df1c717f3f28a2e27ffeaf5428ff063b90';

// export default api;
