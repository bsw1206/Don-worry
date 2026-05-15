import { createRouter, createWebHistory } from 'vue-router'
// 1. 사용할 화면(컴포넌트)들을 불러옵니다.
import HomeView from '../views/HomeView.vue'
import ProductListView from '../views/ProductListView.vue'
import ProductDetailView from '../views/ProductDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      // 메인 페이지: http://localhost:5173/
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      // 상품 목록: http://localhost:5173/products
      path: '/products',
      name: 'product-list',
      component: ProductListView
    },
    {
      // 상품 상세: http://localhost:5173/products/WR0001 (동적 경로)
      // :id 자리에 실제 상품 코드가 들어갑니다.
      path: '/products/:id',
      name: 'product-detail',
      component: ProductDetailView
    },
    {
      // 관심 상품 (나중에 구현할 페이지를 위해 미리 등록)
      path: '/wishlist',
      name: 'wishlist',
      component: () => import('../views/HomeView.vue') // 임시로 홈으로 연결
    }
  ]
})

export default router