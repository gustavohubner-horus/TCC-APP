<template>
  <q-layout style="background-color: #F2F4F3;">
    <q-page-container>
      <q-page class="flex flex-center">
        <q-card flat class="q-pa-xl bg-transparent" style="width: 100%; max-width: 400px;">
          <div class="text-center q-mb-xl">
            <q-avatar size="120px" class="shadow-4" color="white">
              <img src="../assets/branco_fundo_verde.jpeg" alt="Logo do App">
            </q-avatar>
          </div>

          <q-input
            v-model="login"
            label="Login"
            outlined            color="primary"
            class="q-mb-md"
            bg-color="white"
            autocomplete="off"
          >
            <template #prepend>
              <q-icon name="person" />
            </template>
          </q-input>

          <q-input
            v-model="Senha"
            label="Senha"
            :type="exibirSenha ? 'text' : 'password'"
            outlined            color="primary"
            class="q-mb-md"
            bg-color="white"
            autocomplete="new-password"
          >
            <template #prepend>
              <q-icon name="lock" />
            </template>

            <template #append>
              <q-icon
                :name="exibirSenha ? 'visibility' : 'visibility_off'"
                class="cursor-pointer"
                @click="exibirSenha = !exibirSenha"
              />
            </template>
          </q-input>

          <q-btn
            label="Entrar"
            color="primary"
            class="full-width q-mb-md"
            size="lg"            unelevated
            :loading="authStore.loading"
            @click="entrar"
          />

          <q-btn
            label="Cadastrar-se"
            color="primary"
            outline            class="full-width q-mb-md"
            size="lg"
            to="/cadastro"
          />

        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from '@/stores/auth-store'

const login = ref('')
const Senha = ref('')
const exibirSenha = ref(false)

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()

async function entrar() {
  try {
    await authStore.entrar(login.value, Senha.value)
    router.push('/')
  } catch {
    $q.notify({ type: 'negative', message: authStore.error })
  }
}
</script>