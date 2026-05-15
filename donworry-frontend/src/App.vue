<template>
  <div class="bg-gray-50 min-h-screen text-gray-900 font-sans">
    <nav class="bg-white shadow-sm sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <router-link to="/" class="text-2xl font-black text-blue-600 tracking-tighter">
          Don-worry
        </router-link>
        
        <div class="hidden md:flex space-x-8 font-bold text-gray-600">
          <router-link to="/products" class="hover:text-blue-600 transition-colors">상품 조회</router-link>
          <router-link to="/wishlist" class="hover:text-blue-600 transition-colors">관심 상품</router-link>
          <a href="#" class="hover:text-blue-600 transition-colors">금융 뉴스</a>
        </div>
        
        <button class="bg-blue-600 text-white px-5 py-2 rounded-xl font-bold hover:bg-blue-700 transition-all shadow-md shadow-blue-100">
          로그인
        </button>
      </div>
    </nav>

    <div class="bg-gray-900 text-white py-2 overflow-hidden shadow-inner">
      <div class="max-w-7xl mx-auto px-4 flex space-x-8 overflow-x-auto scrollbar-hide items-center h-6">
        <span class="text-xs font-bold text-gray-400 uppercase tracking-widest shrink-0">Live Market</span>
        
        <span v-if="realtimeData.length === 0" class="text-sm font-semibold text-gray-500 animate-pulse">
          초기 데이터 불러오는 중...
        </span>

        <div v-for="(item, index) in realtimeData" :key="index" class="flex items-center space-x-2 text-sm font-semibold shrink-0">
          <span>{{ item.name }}</span>
          
          <span :class="item.change_status === 'RISE' ? 'text-red-400' : (item.change_status === 'FALL' ? 'text-blue-400' : 'text-gray-300')">
            {{ Number(item.price).toLocaleString() }}원
            <span v-if="item.change_status === 'RISE'">▲</span>
            <span v-else-if="item.change_status === 'FALL'">▼</span>
            <span v-else>-</span>
          </span>
        </div>
      </div>
    </div>

    <router-view />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import axios from 'axios'; // 🎯 axios 임포트 (API 통신용)

// 1. 실시간 데이터를 담을 배열
const realtimeData = ref([]);
let socket = null;

onMounted(async () => {
  // 🎯 [추가 1] 페이지 접속 시 기존 데이터를 먼저 가져오기 (API 주소는 백엔드 설정에 맞게 변경하세요)
  try {
    // 임시로 주식 데이터를 가져오는 API 엔드포인트라고 가정합니다.
    const response = await axios.get('http://15.165.238.176:8000/api/v1/products/stocks/'); 
    if (response.data) {
      // 서버에서 가져온 초기 데이터를 티커에 세팅
      // (배열 형태가 아니라면 realtimeData.value = [response.data] 로 묶어주세요)
      realtimeData.value = response.data;
    }
  } catch (err) {
    console.error('기존 데이터 로드 실패 (API를 확인해주세요):', err);
  }

  // 🎯 [추가 2] 실제 EC2 서버 주소로 웹소켓 연결
  socket = new WebSocket('ws://15.165.238.176:8000/ws/products/');

  socket.onopen = () => {
    console.log('✅ 웹소켓 연결 성공! (Global App.vue)');
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    // 🎯 [개선] 3초마다 배열이 늘어나지 않고, '삼성전자'가 이미 있으면 가격만 갱신!
    const existingIndex = realtimeData.value.findIndex(item => item.name === data.name);
    
    if (existingIndex !== -1) {
      // 이미 리스트에 있는 종목이면 데이터 덮어쓰기 (화면 즉시 갱신)
      realtimeData.value[existingIndex] = { ...realtimeData.value[existingIndex], ...data };
    } else {
      // 새로운 종목이면 맨 앞에 추가 (최대 10개 유지)
      realtimeData.value.unshift(data);
      if (realtimeData.value.length > 10) {
        realtimeData.value.pop(); 
      }
    }
  };

  socket.onerror = (error) => {
    console.error('❌ 웹소켓 에러:', error);
  };
});

onUnmounted(() => {
  if (socket) {
    socket.close();
  }
});
</script>

<style scoped>
/* 가로 스크롤바 숨기기 (깔끔한 UI를 위해) */
.scrollbar-hide::-webkit-scrollbar {
    display: none;
}
.scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
</style>