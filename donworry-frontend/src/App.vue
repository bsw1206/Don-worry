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
        
        <div v-for="(item, index) in realtimeData" :key="index" class="flex items-center space-x-2 text-sm font-semibold shrink-0">
          <span>{{ item.name }}</span>
          
          <span :class="item.change === 'RISE' ? 'text-red-400' : (item.change === 'FALL' ? 'text-blue-400' : 'text-gray-300')">
            {{ item.price.toLocaleString() }}원
            <span v-if="item.change === 'RISE'">▲</span>
            <span v-else-if="item.change === 'FALL'">▼</span>
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

// 1. 실시간 데이터를 담을 배열
const realtimeData = ref([]);
let socket = null;

onMounted(() => {
  // 🎯 로컬 테스트용 주소. 나중에는 서버 IP(15.165...)로 변경하세요!
  socket = new WebSocket('ws://localhost:8000/ws/products/');

  socket.onopen = () => {
    console.log('✅ 웹소켓 연결 성공! (Global App.vue)');
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    // 배열 맨 앞에 최신 데이터 추가
    // (만약 종목이 많아지면 배열이 무한정 길어지지 않게 10개만 유지하는 로직)
    realtimeData.value.unshift(data);
    if (realtimeData.value.length > 10) {
      realtimeData.value.pop(); 
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