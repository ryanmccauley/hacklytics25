import axios from "axios"

const http = axios.create({
	baseURL: import.meta.env.VITE_BACKEND_BASE_URL,
})

export default http
