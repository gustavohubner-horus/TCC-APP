<template>
  <q-layout>
    <q-page-container>
      <q-page class="flex flex-center">
        <q-card flat class="q-pa-xl bg-transparent" style="width: 100%; max-width: 400px;">
          <div class="text-center q-mb-lg">
            <q-avatar size="90px" class="shadow-4" color="white">
              <img src="../assets/branco_fundo_verde.jpeg" alt="Logo do App">
            </q-avatar>
          </div>

          <q-input
            v-model="nome"
            label="Nome"
            outlined rounded
            color="primary"
            class="q-mb-md"
            bg-color="white"
          >
            <template #prepend><q-icon name="badge" /></template>
          </q-input>

          <q-input
            v-model="login"
            label="Login"
            outlined rounded
            color="primary"
            class="q-mb-md"
            bg-color="white"
            autocomplete="off"
          >
            <template #prepend><q-icon name="person" /></template>
          </q-input>

          <q-input
            v-model="email"
            label="E-mail"
            type="email"
            outlined rounded
            color="primary"
            class="q-mb-md"
            bg-color="white"
          >
            <template #prepend><q-icon name="email" /></template>
          </q-input>

          <q-input
            v-model="senha"
            label="Senha"
            :type="exibirSenha ? 'text' : 'password'"
            outlined rounded
            color="primary"
            class="q-mb-md"
            bg-color="white"
            autocomplete="new-password"
          >
            <template #prepend><q-icon name="lock" /></template>
            <template #append>
              <q-icon
                :name="exibirSenha ? 'visibility' : 'visibility_off'"
                class="cursor-pointer"
                @click="exibirSenha = !exibirSenha"
              />
            </template>
          </q-input>

          <q-input
            v-model="dataNascimento"
            label="Data de nascimento"
            type="date"
            stack-label
            outlined rounded
            color="primary"
            class="q-mb-md"
            bg-color="white"
          >
            <template #prepend><q-icon name="event" /></template>
          </q-input>

          <q-btn
            label="Cadastrar"
            color="primary"
            class="full-width q-mb-md"
            size="lg"
            rounded unelevated
            :loading="authStore.loading"
            @click="cadastrar"
          />

          <div class="text-center q-mt-md">
            <q-btn
              flat no-caps
              color="primary"
              label="Já tenho conta"
              class="text-weight-bold"
              to="/login"
            />
          </div>

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

const nome = ref('')
const login = ref('')
const email = ref('')
const senha = ref('')
const dataNascimento = ref('')
const exibirSenha = ref(false)

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()

async function cadastrar() {
  try {
    await authStore.cadastrar({
      nome: nome.value,
      login: login.value,
      email: email.value,
      senha: senha.value,
      data_nascimento: dataNascimento.value,
    })
    $q.notify({ type: 'positive', message: 'Cadastro realizado! Faça login.' })
    router.push('/login')
  } catch {
    $q.notify({ type: 'negative', message: authStore.error })
  }
}
</script>