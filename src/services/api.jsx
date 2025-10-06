import axios from "axios";

const API = axios.create({
      baseURL: "https://chart.dsrt321.online/api",
      headers: { "Content-Type": "application/json" },
});

// Attach JWT token automatically
API.interceptors.request.use((config) => {
      const token = localStorage.getItem("access_token");
      if (token) config.headers.Authorization = `Bearer ${token}`;
      return config;
});

// Handle 401 globally
API.interceptors.response.use(
      (response) => response,
      (error) => {
            if (error.response?.status === 401) {
                  localStorage.removeItem("user");
                  localStorage.removeItem("access_token");
                  window.location.href = "/login";
            }
            return Promise.reject(error);
      }
);

export default API;
