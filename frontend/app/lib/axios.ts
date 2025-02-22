import axios from "axios";

const http = axios.create({
  baseURL: process.env.VITE_BACKEND_BASE_URL,
})

export default http