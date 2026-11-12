const routes = [
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('@/pages/IndexPage.vue') },
      { path: 'gastos', component: () => import('@/pages/GastosPage.vue') },
      { path: 'cadastros', component: () => import('@/pages/CadastrosPage.vue') },
      { path: 'cadastros/categorias', component: () => import('@/pages/CategoriasPage.vue') },
      { path: 'cadastros/limites', component: () => import('@/pages/LimitesPage.vue') },
      { path: 'cadastros/gastos-fixos', component: () => import('@/pages/GastosFixosPage.vue') },
      { path: 'grupos', component: () => import('@/pages/GruposPage.vue') },
      { path: 'grupos/:id', component: () => import('@/pages/GrupoDetalhePage.vue') },
      { path: 'perfil', component: () => import('@/pages/PerfilPage.vue') },
    ],
  },

  {
    path: '/login',
    component: () => import('../pages/LoginPage.vue'),
  },
  {
    path: '/cadastro',
    component: () => import('@/pages/CadastroPage.vue'),
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('@/pages/ErrorNotFound.vue'),
  },
]

export default routes
