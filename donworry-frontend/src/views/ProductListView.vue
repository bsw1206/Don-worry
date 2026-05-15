<template>
  <main class="max-w-7xl mx-auto px-4 py-16">
    <div class="flex flex-col md:flex-row justify-between items-end mb-12 gap-4">
      <div>
        <h2 class="text-4xl font-black mb-2 tracking-tight text-gray-900">전체 상품 조회</h2>
        <p class="text-gray-500 font-medium text-lg">국내 주요 은행의 모든 정기예금 상품을 한눈에 비교하세요.</p>
      </div>
      <div class="bg-white p-2 rounded-2xl shadow-sm border border-gray-100 flex gap-2">
        <button class="px-6 py-2 bg-blue-600 text-white rounded-xl font-bold">정기예금</button>
        <button class="px-6 py-2 text-gray-400 font-bold hover:bg-gray-50 rounded-xl transition-colors">적금</button>
      </div>
    </div>

    <div v-if="products.length === 0" class="text-center py-32 bg-white rounded-3xl border border-dashed border-gray-200">
      <p class="text-gray-400 font-bold text-xl">상품 데이터를 불러오고 있습니다...</p>
    </div>

    <div v-else class="grid grid-cols-1 gap-6">
      <div v-for="p in products" :key="p.fin_prdt_cd" 
           class="group bg-white p-8 rounded-3xl shadow-sm border border-gray-100 flex flex-col md:flex-row justify-between items-center hover:border-blue-400 hover:shadow-xl hover:shadow-blue-50/50 transition-all duration-300">
        <div class="w-full">
          <div class="flex items-center gap-3 mb-3">
            <span class="text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded-full font-black uppercase tracking-wider">{{ p.bank_name }}</span>
            <span class="text-xs bg-gray-100 text-gray-500 px-3 py-1 rounded-full font-bold">정기예금</span>
          </div>
          <h3 class="text-2xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors">{{ p.fin_prdt_nm }}</h3>
          <p class="text-gray-500 mt-2 font-medium">가입 방법: {{ p.join_way }}</p>
        </div>
        
        <div class="w-full md:w-auto mt-6 md:mt-0 text-right flex md:flex-col items-center md:items-end justify-between gap-6 border-t md:border-t-0 pt-6 md:pt-0 border-gray-50">
          <div>
            <div class="text-sm text-gray-400 font-bold mb-1">최고 금리</div>
            <div class="text-4xl font-black text-red-500">{{ p.options[0]?.intr_rate2 || '0.0' }}<span class="text-xl">%</span></div>
          </div>
          <router-link :to="{ name: 'product-detail', params: { id: p.fin_prdt_cd } }" 
                       class="bg-gray-900 text-white px-8 py-3 rounded-2xl font-bold hover:bg-blue-600 transition-all active:scale-95 whitespace-nowrap">
            자세히 보기
          </router-link>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const products = ref([])

onMounted(async () => {
  try {
    // 로컬 주소로 접속할 때
    // const res = await axios.get('http://localhost:8000/api/products/')
    // 서버 주소로 접속할 때
    const res = await axios.get('http://54.180.53.205:8000/api/products/')

    products.value = res.data
  } catch (err) {
    console.error(err)
  }
})
</script>