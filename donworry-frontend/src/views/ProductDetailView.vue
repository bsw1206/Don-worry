<template>
  <main class="max-w-5xl mx-auto px-4 py-16" v-if="product">
    <div class="mb-12">
      <button @click="$router.go(-1)" class="group text-gray-400 font-bold flex items-center gap-2 hover:text-blue-600 transition-colors mb-6">
        <span class="text-xl group-hover:-translate-x-1 transition-transform">←</span> 상품 목록으로 돌아가기
      </button>
      
      <div class="flex items-center gap-3 mb-4">
        <span class="bg-blue-600 text-white text-xs px-3 py-1 rounded-lg font-black tracking-widest">{{ product.bank_name }}</span>
      </div>
      <h1 class="text-5xl font-black text-gray-900 mb-6">{{ product.fin_prdt_nm }}</h1>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
      <div class="lg:col-span-2 space-y-10">
        <div class="bg-white p-10 rounded-[2.5rem] shadow-sm border border-gray-100">
          <h3 class="text-2xl font-bold mb-8 flex items-center gap-2">
            <span class="p-2 bg-blue-50 rounded-xl">📄</span> 상품 상세 안내
          </h3>
          <div class="space-y-8">
            <div>
              <h4 class="text-gray-400 text-sm font-black mb-2 uppercase tracking-widest">가입 방법</h4>
              <p class="text-xl font-bold text-gray-800">{{ product.join_way }}</p>
            </div>
            <div>
              <h4 class="text-gray-400 text-sm font-black mb-2 uppercase tracking-widest">우대 조건</h4>
              <p class="text-gray-700 leading-relaxed text-lg">{{ product.spcl_cnd }}</p>
            </div>
            <div>
              <h4 class="text-gray-400 text-sm font-black mb-2 uppercase tracking-widest">가입 대상</h4>
              <p class="text-gray-700 leading-relaxed text-lg">{{ product.join_member }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="space-y-6">
        <div class="bg-gray-900 text-white p-8 rounded-[2.5rem] shadow-xl">
          <h3 class="text-lg font-bold text-blue-400 mb-6 uppercase tracking-widest">Interest Rates</h3>
          <div class="space-y-4">
            <div v-for="opt in product.options" :key="opt.id" class="flex justify-between items-center border-b border-gray-800 pb-4">
              <div>
                <span class="text-2xl font-black">{{ opt.save_trm }}</span>
                <span class="text-gray-500 font-bold ml-1 text-sm">MONTHS</span>
              </div>
              <div class="text-right">
                <div class="text-xs text-gray-500 font-bold">MAX RATE</div>
                <div class="text-2xl font-black text-red-500">{{ opt.intr_rate2 }}%</div>
              </div>
            </div>
          </div>
          <button class="w-full bg-blue-600 text-white py-4 rounded-2xl font-bold mt-8 hover:bg-blue-700 transition-colors">
            이 상품 찜하기
          </button>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const product = ref(null)

onMounted(async () => {
  try {
    const res = await axios.get(`http://localhost:8000/api/products/${route.params.id}/`)
    product.value = res.data
  } catch (err) {
    console.error(err)
  }
})
</script>