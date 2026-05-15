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

    <router-view />
  </div>
</template>

<script setup>
// 공통 레이아웃으로 별도의 로직은 필요 없습니다.
</script>