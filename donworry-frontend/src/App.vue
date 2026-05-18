<template>
  <div class="bg-gray-50 min-h-screen text-gray-900 font-sans">
    <nav class="bg-white shadow-sm sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <router-link to="/" class="text-2xl font-black text-blue-600 tracking-tighter">
          Don-worry
        </router-link>
        
        <div class="hidden md:flex space-x-8 font-bold text-gray-600">
          <router-link to="/products" class="hover:text-blue-600 transition-colors">상품 조회</router-link>
          <button @click="handleWishlistClick" class="hover:text-blue-600 transition-colors font-bold">
            관심 상품
          </button>
          <a href="#" class="hover:text-blue-600 transition-colors">금융 뉴스</a>
        </div>
        
        <button 
          v-if="!isLoggedIn"
          @click="$router.push('/login')"
          class="bg-blue-600 text-white px-5 py-2 rounded-xl font-bold hover:bg-blue-700 transition-all shadow-md shadow-blue-100"
        >
          로그인
        </button>
        <button 
          v-else
          @click="handleLogout"
          class="bg-gray-200 text-gray-700 px-5 py-2 rounded-xl font-bold hover:bg-gray-300 transition-all"
        >
          로그아웃
        </button>
      </div>
    </nav>

    <div class="bg-gray-900 text-white py-2 overflow-hidden shadow-inner">
      <div class="max-w-7xl mx-auto px-4 flex space-x-8 overflow-x-auto scrollbar-hide items-center h-6">
        <span class="text-xs font-bold text-gray-400 uppercase tracking-widest shrink-0">Live Market</span>
        <div v-for="(item, index) in realtimeData" :key="index" class="flex items-center space-x-2 text-sm font-semibold shrink-0">
          <span>{{ item.name }}</span>
          <span :class="item.change_status === 'RISE' ? 'text-red-400' : (item.change_status === 'FALL' ? 'text-blue-400' : 'text-gray-300')">
            {{ Number(item.price).toLocaleString() }}원
          </span>
        </div>
      </div>
    </div>

    <router-view />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const realtimeData = ref([{ name: '삼성전자', price: 74500, change_status: 'RISE' }]);
const isLoggedIn = ref(false);

onMounted(() => {
  // 로컬 스토리지에 토큰이 있는지 확인하여 로그인 상태 결정
  isLoggedIn.value = !!localStorage.getItem('token');
});

// 관심 상품 네비게이션 가드 구현
const handleWishlistClick = () => {
  if (!isLoggedIn.value) {
    alert('로그인이 필요한 서비스입니다. 로그인 페이지로 이동해요! 🔒');
    router.push('/login');
  } else {
    router.push('/wishlist');
  }
};

// 로그아웃 시스템 구현
const handleLogout = () => {
  localStorage.removeItem('token');
  isLoggedIn.value = false;
  alert('안전하게 로그아웃 되었습니다. 다음에 또 만나요! 🐷');
  router.push('/');
  window.location.reload(); // 메인 화면 컴포넌트의 상태를 한 번에 동기화하기 위해 리로드 처리
};
</script>