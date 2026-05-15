<template>
  <div>
    <header class="bg-blue-600 text-white py-20 px-4">
      <div class="max-w-7xl mx-auto text-center">
        <h1 class="text-5xl font-black mb-6 leading-tight">
          내 자산의 가치를 높이는<br />최적의 금융 파트너
        </h1>
        <p class="text-blue-100 text-lg mb-10 opacity-90">정기예금 · 적금 · 주식 데이터를 실시간으로 비교하고 추천받으세요.</p>
        <div class="flex justify-center gap-4">
          <router-link to="/products" class="bg-white text-blue-600 px-8 py-4 rounded-full font-bold shadow-xl hover:scale-105 transition-transform">
            상품 전체 둘러보기
          </router-link>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-16">
      <section class="mb-20">
        <h2 class="text-2xl font-bold mb-8 flex items-center gap-2">
          <span class="text-3xl">🔥</span> 현재 금리 TOP 3 상품
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="(p, index) in topProducts" :key="p.fin_prdt_cd" 
               class="bg-white p-8 rounded-3xl shadow-sm border border-gray-100 relative overflow-hidden hover:shadow-lg transition-shadow">
            <div class="absolute top-0 left-0 bg-blue-600 text-white px-4 py-1 text-xs font-bold rounded-br-xl">TOP {{ index + 1 }}</div>
            <div class="text-sm text-gray-400 mt-2 mb-1">{{ p.bank_name }}</div>
            <div class="text-xl font-bold mb-4 truncate">{{ p.fin_prdt_nm }}</div>
            <div class="text-4xl font-black text-blue-600 mb-2">
              {{ p.options[0]?.intr_rate2 || '0.0' }}%
            </div>
            <div class="text-sm text-gray-400">최고 금리 기준 (12개월)</div>
          </div>
        </div>
      </section>

      <section class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
        <div class="bg-white p-8 rounded-3xl shadow-sm border border-gray-100 h-full">
          <h3 class="text-xl font-bold mb-6">📈 실시간 증시 요약</h3>
          <div v-if="stockData.prices.length > 0">
            <div class="flex justify-between items-end mb-6">
              <div>
                <p class="text-gray-400 font-bold uppercase tracking-wider text-sm">SAMSUNG ELECTRONICS</p>
                <h4 class="text-4xl font-black mt-1">삼성전자</h4>
              </div>
              <div class="text-right">
                <p class="text-3xl font-black text-blue-600">{{ stockData.prices[stockData.prices.length - 1] }}원</p>
                <p class="text-sm text-gray-400">업데이트: {{ lastUpdated }}</p>
              </div>
            </div>
          </div>
          <div class="h-64">
            <canvas id="mainStockChart"></canvas>
          </div>
        </div>

        <div class="bg-blue-50 p-8 rounded-3xl h-full flex flex-col justify-center">
          <h3 class="text-2xl font-bold mb-4 text-blue-900">맞춤 추천이 필요하신가요?</h3>
          <p class="text-blue-700 mb-8 leading-relaxed">승우님의 투자 성향과 목표 자산을 분석하여 지금 가장 유리한 상품을 찾아드립니다. 1분이면 충분해요!</p>
          <button class="bg-blue-600 text-white w-full py-4 rounded-2xl font-bold text-lg hover:bg-blue-700 transition-colors">
            성향 설문 시작하기
          </button>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import Chart from 'chart.js/auto'

const products = ref([])
const stockData = ref({ labels: [], prices: [] })
let chartInstance = null
let timer = null

const topProducts = computed(() => {
  return [...products.value]
    .sort((a, b) => (b.options[0]?.intr_rate2 || 0) - (a.options[0]?.intr_rate2 || 0))
    .slice(0, 3)
})

const lastUpdated = computed(() => stockData.value.labels[stockData.value.labels.length - 1] || '-')

const fetchData = async () => {
  try {
    const [prodRes, stockRes] = await Promise.all([
      axios.get('http://localhost:8000/api/products/'),
      axios.get('http://localhost:8000/api/stock-chart-data/')
    ])
    products.value = prodRes.data
    stockData.value = stockRes.data
    
    if (chartInstance) {
      chartInstance.data.labels = stockRes.data.labels
      chartInstance.data.datasets[0].data = stockRes.data.prices
      chartInstance.update()
    }
  } catch (err) {
    console.error(err)
  }
}

onMounted(() => {
  fetchData()
  const ctx = document.getElementById('mainStockChart')
  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: '주가',
        data: [],
        borderColor: '#2563eb',
        borderWidth: 3,
        pointRadius: 0,
        fill: true,
        backgroundColor: 'rgba(37, 99, 235, 0.05)',
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { x: { display: false }, y: { grid: { display: false } } }
    }
  })
  timer = setInterval(fetchData, 3000)
})

onUnmounted(() => { clearInterval(timer) })
</script>