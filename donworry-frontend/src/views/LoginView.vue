<template>
  <main class="min-h-screen bg-[#e0f2fe] flex items-center justify-center px-4 py-12 relative overflow-hidden">
    
    <div class="absolute top-[-10%] left-[-5%] w-64 h-64 bg-[#fef08a] rounded-full opacity-40 blur-3xl"></div>
    <div class="absolute bottom-[-10%] right-[-5%] w-80 h-80 bg-[#ffedd5] rounded-full opacity-50 blur-3xl"></div>

    <div class="w-full max-w-md relative z-10">
      <div class="flex justify-center mb-[-40px] relative z-20">
        
      </div>

      <div class="bg-white p-10 pt-16 rounded-[3rem] shadow-[0_20px_50px_rgba(59,130,246,0.15)] border-4 border-[#bae6fd]">
        
        <div class="text-center mb-8">
          <h2 class="text-3xl font-black text-[#0c4a6e] mb-2 tracking-tight">반가워요! </h2>
          <p class="text-[#7dd3fc] font-bold text-sm">돈 걱정은 뚝, Don-worry와 함께해요</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <label class="block text-[#0ea5e9] text-xs font-black uppercase tracking-widest ml-4 mb-2">이메일</label>
            <input 
              v-model="email"
              type="email" 
              required
              placeholder="hello@donworry.com" 
              class="w-full bg-[#f0f9ff] border-2 border-transparent focus:border-[#7dd3fc] text-[#0369a1] px-6 py-4 rounded-[2rem] text-base focus:outline-none transition-all placeholder:text-[#bae6fd] font-bold"
            />
          </div>

          <div>
            <label class="block text-[#0ea5e9] text-xs font-black uppercase tracking-widest ml-4 mb-2">비밀번호</label>
            <input 
              v-model="password"
              type="password" 
              required
              placeholder="비밀번호를 속닥속닥" 
              class="w-full bg-[#f0f9ff] border-2 border-transparent focus:border-[#7dd3fc] text-[#0369a1] px-6 py-4 rounded-[2rem] text-base focus:outline-none transition-all placeholder:text-[#bae6fd] font-bold"
            />
          </div>

          <button 
            type="submit" 
            class="w-full bg-[#3b82f6] hover:bg-[#2563eb] text-white font-black py-4 rounded-[2rem] text-lg transition-all active:scale-[0.95] shadow-[0_10px_20px_rgba(59,130,246,0.3)] flex items-center justify-center gap-2"
          >
            시작하기 
          </button>
        </form>

        <div class="relative flex py-8 items-center">
          <div class="flex-grow border-t-2 border-[#f0f9ff]"></div>
          <span class="flex-shrink mx-4 text-[#bae6fd] text-sm font-black">또는</span>
          <div class="flex-grow border-t-2 border-[#f0f9ff]"></div>
        </div>

        <button 
          @click="handleGoogleLogin"
          type="button"
          class="w-full bg-white border-2 border-[#f0f9ff] hover:bg-[#f8fafc] text-[#64748b] font-bold py-3.5 rounded-[2rem] text-sm flex items-center justify-center gap-3 transition-all active:scale-[0.95]"
        >
          <img src="https://www.google.com/favicon.ico" class="w-4 h-4" />
          구글로 간편하게 오기
        </button>

        <div class="mt-8 text-center text-sm font-bold text-[#94a3b8]">
          계정이 없으신가요? 
          <router-link to="/signup" class="text-[#3b82f6] font-black hover:underline ml-2">회원가입</router-link>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const email = ref('');
const password = ref('');

const handleLogin = async () => {
  // 로그인 로직...
  alert('로그인 성공! 환영해요 🍀');
  router.push('/');
};

const handleGoogleLogin = () => {
  alert('구글 친구들과 연결 중...');
};
</script>