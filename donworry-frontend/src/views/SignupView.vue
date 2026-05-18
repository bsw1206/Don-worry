<template>
  <main class="max-w-lg mx-auto px-4 py-16">
    <div class="bg-white p-10 rounded-[2.5rem] shadow-sm border border-gray-100">
      <div class="text-center mb-10">
        <h2 class="text-3xl font-black tracking-tight text-gray-900 mb-2">시작하기</h2>
        <p class="text-gray-400 font-medium text-sm">기본 정보를 입력하고 맞춤 자산 관리를 받아보세요.</p>
      </div>

      <form @submit.prevent="handleSignup" class="space-y-6">
        <div>
          <label class="text-xs font-black text-gray-400 uppercase tracking-widest block mb-2">이메일 (ID)</label>
          <input 
            v-model="form.email" 
            type="email" 
            required 
            placeholder="example@email.com" 
            class="w-full px-5 py-4 bg-gray-50 border border-gray-200 rounded-2xl font-medium focus:outline-none focus:border-blue-500 focus:bg-white transition-all text-base"
          />
        </div>
        
        <div>
          <label class="text-xs font-black text-gray-400 uppercase tracking-widest block mb-2">비밀번호</label>
          <input 
            v-model="form.password" 
            type="password" 
            required 
            placeholder="••••••••" 
            class="w-full px-5 py-4 bg-gray-50 border border-gray-200 rounded-2xl font-medium focus:outline-none focus:border-blue-500 focus:bg-white transition-all text-base"
          />
        </div>
        
        <div>
          <label class="text-xs font-black text-gray-400 uppercase tracking-widest block mb-2">닉네임</label>
          <input 
            v-model="form.nickname" 
            type="text" 
            required 
            placeholder="돈워리맨" 
            class="w-full px-5 py-4 bg-gray-50 border border-gray-200 rounded-2xl font-medium focus:outline-none focus:border-blue-500 focus:bg-white transition-all text-base"
          />
        </div>

        <div>
          <label class="text-xs font-black text-gray-400 uppercase tracking-widest block mb-2">나이대</label>
          <div class="grid grid-cols-2 gap-3">
            <button 
              type="button" 
              v-for="age in ['20대', '30대', '40대', '50대 이상']" 
              :key="age"
              @click="form.age_group = age"
              :class="form.age_group === age 
                ? 'py-3 border-2 border-blue-600 rounded-xl font-bold text-blue-600 bg-blue-50/50 transition-colors text-sm' 
                : 'py-3 border border-gray-200 rounded-xl font-bold text-gray-500 bg-white hover:bg-gray-50 transition-colors text-sm'"
            >
              {{ age }}
            </button>
          </div>
        </div>

        <div>
          <label class="text-xs font-black text-gray-400 uppercase tracking-widest block mb-2">월 소득 수준</label>
          <div class="grid grid-cols-1 gap-3">
            <button 
              type="button" 
              v-for="income in ['200만 미만', '200~400만', '400만 이상']" 
              :key="income"
              @click="form.income_level = income"
              :class="form.income_level === income 
                ? 'py-3 border-2 border-blue-600 rounded-xl font-bold text-blue-600 bg-blue-50/50 transition-colors text-sm' 
                : 'py-3 border border-gray-200 rounded-xl font-bold text-gray-500 bg-white hover:bg-gray-50 transition-colors text-sm'"
            >
              {{ income }}
            </button>
          </div>
        </div>

        <button 
          type="submit" 
          class="w-full bg-blue-600 text-white py-4 rounded-2xl font-bold hover:bg-blue-700 transition-all active:scale-[0.98] shadow-lg shadow-blue-100 text-lg mt-4"
        >
          가입 완료하기
        </button>
      </form>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const form = ref({
  email: '',
  password: '',
  nickname: '',
  age_group: '20대',
  income_level: '200~400만'
});

const handleSignup = async () => {
  try {
    // 🎯 회원가입 성공 시 메인 화면으로 이동하면서 가입 유저 신호를 주입합니다.
    router.push({ path: '/', query: { newuser: 'true' } });
  } catch (err) {
    console.error(err);
    alert('회원가입 실패: 입력 항목을 다시 확인해주세요.');
  }
};
</script>