<template>
  <div>
    <div class="p-6">
       </div>

    <transition name="slide-up">
      <div v-if="showSurveyOffer" class="fixed bottom-0 left-0 right-0 z-[100] p-6 pointer-events-none">
        <div class="max-w-xl mx-auto bg-gray-900 text-white p-6 rounded-[2rem] shadow-2xl shadow-blue-900/20 border border-gray-800 pointer-events-auto flex items-center justify-between gap-6">
          <div class="flex items-center gap-4">
            <div class="bg-blue-600 p-3 rounded-2xl text-2xl">🤔</div>
            <div>
              <h4 class="font-black text-lg leading-tight">잠깐! 성향 조사를 하셨나요?</h4>
              <p class="text-gray-400 text-sm font-medium">선호도를 파악하여 딱 맞는 상품을 추천해 드릴게요.</p>
            </div>
          </div>
          
          <div class="flex items-center gap-2">
            <button @click="showSurveyOffer = false" class="text-gray-500 hover:text-white px-3 py-2 font-bold text-sm">다음에</button>
            <router-link to="/survey" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-black text-sm transition-all whitespace-nowrap">
              조사하기
            </router-link>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const showSurveyOffer = ref(false);

onMounted(() => {
  // ✅ 주소창에 ?newuser=true 가 있으면 1초 뒤에 알림창을 쓱 올림
  if (route.query.newuser === 'true') {
    setTimeout(() => {
      showSurveyOffer.value = true;
    }, 1000); // 메인 화면이 보이고 1초 뒤에 나오는게 더 자연스럽습니다.
  }
});
</script>

<style scoped>
/* ✅ 쓱 올라오는 애니메이션 설정 */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>