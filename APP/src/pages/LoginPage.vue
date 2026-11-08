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
            outlined
            rounded
            color="primary"
            class="q-mb-md"
            bg-color="white"
            >
            <template #prepend>
                <q-icon name="person" />
            </template>
            </q-input>

            <q-input 
              v-model="password" 
              label="Senha" 
              type="password" 
              outlined 
              rounded
              color="primary" 
              class="q-mb-md" 
              bg-color="white"
            >
              <template #prepend>
                <q-icon name="lock" />
              </template>
            </q-input>

            <q-btn 
              label="Entrar" 
              color="primary" 
              class="full-width q-mb-md" 
              size="lg" 
              rounded
              unelevated 
            />

            <q-btn 
              label="Cadastrar-se" 
              color="primary" 
              outline 
              rounded
              class="full-width q-mb-md" 
              size="lg" 
            />
            
            <div class="text-center q-mt-md">
              <q-btn 
                flat 
                color="primary" 
                label="Esqueceu a senha?" 
                class="text-weight-bold"
                no-caps
              />
            </div>

        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'

const login = ref('')
const password = ref('')
</script>
