<template>
  <main class="max-w-4xl mx-auto px-4 py-16">
    <div v-if="!showResult" class="bg-white p-10 rounded-[2.5rem] shadow-sm border border-gray-100 max-w-xl mx-auto">
      <div class="flex justify-between items-center mb-8">
        <span class="text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded-full font-black tracking-widest">INVESTMENT TEST</span>
        <span class="text-sm font-bold text-gray-400">{{ currentStep + 1 }} / {{ questions.length }}</span>
      </div>

      <div class="mb-8">
        <h2 class="text-2xl font-black text-gray-900 leading-snug break-keep">
          {{ questions[currentStep].title }}
        </h2>
      </div>

      <div class="space-y-3">
        <button 
          v-for="opt in questions[currentStep].options" :key="opt.score"
          @click="selectOption(opt.score)"
          class="w-full text-left p-5 border border-gray-200 rounded-2xl font-bold text-gray-700 hover:border-blue-500 hover:bg-blue-50/30 transition-all active:scale-[0.99] text-base"
        >
          {{ opt.text }}
        </button>
      </div>
    </div>

    <div v-else class="space-y-10">
      <div class="bg-white p-12 rounded-[2.5rem] shadow-sm border border-gray-100 text-center">
        <p class="text-gray-400 font-bold text-lg mb-2">회원님의 투자 위험도 결과 (총 {{ totalScore }}점)</p>
        <h1 class="text-5xl font-black text-blue-600 tracking-tight mb-6">
          "{{ resultType }}"
        </h1>
        <p class="text-xl font-bold text-gray-700 max-w-xl mx-auto break-keep leading-relaxed">
          {{ resultDescription }}
        </p>
      </div>

      <div>
        <h3 class="text-xs font-black text-gray-400 uppercase tracking-widest mb-6">─── 맞춤 저축 상품 추천 ───────────────────</h3>
       <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div v-for="product in mockRecommendations" :key="product.fin_prdt_cd" class="bg-white p-8 rounded-3xl shadow-sm border border-gray-100 flex flex-col justify-between hover:shadow-md transition-shadow">
          <div>
            <span class="text-xs bg-gray-100 text-gray-500 px-2.5 py-1 rounded-lg font-bold mb-3 inline-block">
              {{ product.bank }}
            </span>
            <h4 class="text-xl font-bold text-gray-900 mb-2 truncate">{{ product.name }}</h4>
            <div class="text-3xl font-black text-red-500 mb-6">★ {{ product.rate }}%</div>
          </div>
          
          <router-link 
            :to="{ name: 'product-detail', params: { id: product.fin_prdt_cd } }"
            class="w-full text-center bg-gray-50 hover:bg-blue-600 hover:text-white text-gray-900 py-3 rounded-xl font-bold text-sm transition-colors block"
          >
            상세 보기
          </router-link>
        </div>
        </div>
      </div>

      <div class="bg-gray-900 text-white p-10 rounded-[2.5rem] shadow-xl flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div>
          <h4 class="text-lg font-black text-blue-400 uppercase tracking-widest mb-2">─── ETF도 살펴보세요 ───────────────────</h4>
          <p class="text-lg font-bold text-gray-300">주식형 ETF부터 채권형 ETF까지, 다양한 ETF 상품을 비교해 보세요.</p>
          <p class="text-sm text-gray-500 mt-1 font-medium">※ 회원님의 위험도 점수를 반영한 ETF 추천도 확인할 수 있어요. (원금 손실 가능성 유의)</p>
        </div>
        <router-link to="/products" class="bg-blue-600 text-white px-6 py-4 rounded-xl font-black text-base hover:bg-blue-700 transition-colors whitespace-nowrap shrink-0">
          ETF 페이지 둘러보기 →
        </router-link>
      </div>

      
    </div>
  </main>
</template>

<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';

// 1. 기획서 점수 및 문항 완전 반영
const questions = [
  {
    title: "Q1. 투자 목적은 무엇인가요?",
    options: [
      { text: "① 원금 보전이 최우선이다", score: 1 },
      { text: "② 안정적인 이자 수익을 원한다", score: 3 },
      { text: "③ 시장 수익률 수준을 기대한다", score: 5 },
      { text: "④ 높은 수익을 위해 손실도 감수할 수 있다", score: 7 },
    ]
  },
  {
    title: "Q2. 투자 가능 기간은 얼마나 되나요?",
    options: [
      { text: "① 6개월 미만", score: 1 },
      { text: "② 6개월~1년", score: 2 },
      { text: "③ 1~3년", score: 4 },
      { text: "④ 3년 이상", score: 6 },
    ]
  },
  {
    title: "Q3. 다음 상황에서 어떻게 행동하겠습니까? (투자 상품이 20% 손실이 발생했을 때)",
    options: [
      { text: "① 즉시 전액 환매한다", score: 1 },
      { text: "② 일부만 환매한다", score: 2 },
      { text: "③ 유지하며 추이를 지켜본다", score: 4 },
      { text: "④ 오히려 추가 투자한다", score: 6 },
    ]
  },
  {
    title: "Q4. 월 저축 가능 금액은 얼마인가요?",
    options: [
      { text: "① 10만원 미만", score: 1 },
      { text: "② 10~30만원", score: 2 },
      { text: "③ 30~50만원", score: 4 },
      { text: "④ 50만원 이상", score: 5 },
    ]
  },
  {
    title: "Q5. 저축 목적은 무엇인가요?",
    options: [
      { text: "① 비상금·단기 목돈", score: 1 },
      { text: "② 중장기 자산 증식", score: 3 },
      { text: "③ 노후 대비", score: 4 },
      { text: "④ 공격적 자산 증대", score: 6 },
    ]
  }
];

const currentStep = ref(0);
const scoreList = ref([]);
const showResult = ref(false);
const totalScore = ref(0);

// 옵션 선택 처리 시퀀스
const selectOption = async (score) => {
  scoreList.value.push(score);
  
  if (currentStep.value < questions.length - 1) {
    currentStep.value++;
  } else {
    // 모든 문항 완료 -> 합산 연산
    totalScore.value = scoreList.value.reduce((acc, curr) => acc + curr, 0);
    
    try {
      // 🎯 기획서대로 점수 계산서 및 결과는 비동기로 서버에 전송 후 세이브 처리 가능
      // await axios.post('http://localhost:8000/api/v1/survey/', { total_score: totalScore.value });
    } catch (err) {
      console.error(err);
    }
    showResult.value = true;
  }
};

// 점수 기반 판정 기준 분기 계산
const resultType = computed(() => {
  if (totalScore.value <= 14) return "안정형";
  if (totalScore.value <= 24) return "중립형";
  return "수익추구형";
});

const resultDescription = computed(() => {
  if (resultType.value === "안정형") return "원금 보전을 중시하고 안정적인 이자 수익을 선호하는 성향입니다.";
  if (resultType.value === "중립형") return "안정성과 수익성 사이의 균형을 추구하는 성향입니다.";
  return "높은 수익을 위해 일정 수준의 위험을 감수할 의향이 있는 성향입니다.";
});

// 결과용 더미 추천 예적금 카드 데이터
const mockRecommendations = [
  { fin_prdt_cd: "WR00018", bank: "우리은행", name: "WON플러스예금", rate: "4.50" },
  { fin_prdt_cd: "003000", bank: "신한은행", name: "쏠편한 정기적금", rate: "5.20" },
  { fin_prdt_cd: "004000", bank: "국민은행", name: "KB 국민대박 연금저축", rate: "3.80" },
];
</script>