const hostname = window.location.hostname; 
const isVueDev = window.location.port === '5173'; // Vite 기본 포트

// 개발 서버일 때는 백엔드 포트(8000)를 강제하고, 빌드 후 서빙될 때는 브라우저 주소를 그대로 따릅니다.
const BACKEND_BASE = isVueDev ? `${hostname}:8000` : window.location.host;

export const API_BASE_URL = `http://${BACKEND_BASE}/api/v1/products`;
export const WS_BASE_URL = `ws://${BACKEND_BASE}/ws/products/`;