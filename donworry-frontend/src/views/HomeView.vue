<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">실시간 주식 정보</h1>

    <div v-if="stockData" class="bg-gray-800 text-white p-6 rounded-lg shadow-lg w-80">
      <div class="flex justify-between items-center">
        <span class="text-xl font-semibold">{{ stockData.name }}</span>
        <span class="text-sm text-gray-400">실시간</span>
      </div>
      
      <div class="mt-4 flex items-baseline">
        <span class="text-3xl font-bold">
          {{ Number(stockData.price).toLocaleString() }}원
        </span>
        
        <span 
          class="ml-2 text-lg font-bold"
          :class="stockData.change_status === 'RISE' ? 'text-red-500' : (stockData.change_status === 'FALL' ? 'text-blue-500' : 'text-gray-400')"
        >
          <span v-if="stockData.change_status === 'RISE'">▲</span>
          <span v-else-if="stockData.change_status === 'FALL'">▼</span>
          <span v-else>-</span>
        </span>
      </div>
      
      <div class="mt-2 text-xs text-gray-500">
        최근 업데이트: {{ new Date(stockData.timestamp * 1000).toLocaleTimeString() }}
      </div>
    </div>

    <div v-else class="text-gray-500 animate-pulse">
      데이터 수신 대기 중...
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

// 🎯 데이터를 저장할 반응형 변수
const stockData = ref(null);
let socket = null;

onMounted(async () => {
  // 1. 우선 DB에 저장된 기존 데이터를 API로 가져오기 (이게 있어야 처음에 바로 뜸!)
  try {
    const response = await axios.get('http://15.165.238.176:8000/api/v1/products/stocks/');
    stockData.value = response.data[0]; // 가장 최근 데이터 하나 넣기
  } catch (err) {
    console.error("기존 데이터 로드 실패", err);
  }

  // 2. 그 다음 실시간 웹소켓 연결
  const socketUrl = 'ws://15.165.238.176:8000/ws/products/';
  socket = new WebSocket(socketUrl);

  // 메시지를 받았을 때 실행되는 함수
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("수신 데이터:", data); // 브라우저 콘솔에서 확인용
    
    // 🎯 받아온 데이터를 변수에 저장 -> 화면 자동 갱신!
    stockData.value = data;
  };

  socket.onopen = () => console.log("✅ 웹소켓 연결 성공!");
  socket.onclose = () => console.log("❌ 웹소켓 연결 종료");
  socket.onerror = (err) => console.error("🚨 웹소켓 에러:", err);
});

// 페이지를 나갈 때 소켓 닫기
onUnmounted(() => {
  if (socket) socket.close();
});
</script>