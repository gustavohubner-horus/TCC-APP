<template>
  <q-page class="q-pa-md">
    <div class="text-center q-mb-lg">
      <q-icon name="account_circle" size="96px" color="primary" />
      <div class="text-h6 q-mt-sm">{{ authStore.usuario?.usu_nome }}</div>
      <div class="text-caption text-grey">{{ authStore.usuario?.usu_login }}</div>
    </div>

    <q-list bordered separator class="rounded-borders bg-white">
      <q-item>
        <q-item-section avatar>
          <q-icon name="email" color="primary" />
        </q-item-section>
        <q-item-section>
          <q-item-label caption>E-mail</q-item-label>
          <q-item-label>{{ authStore.usuario?.usu_email }}</q-item-label>
        </q-item-section>
      </q-item>

      <q-item clickable v-ripple @click="abrirSenha">
        <q-item-section avatar>
          <q-icon name="lock" color="primary" />
        </q-item-section>
        <q-item-section>Alterar senha</q-item-section>
        <q-item-section side>
          <q-icon name="chevron_right" />
        </q-item-section>
      </q-item>
    </q-list>

    <q-btn
      outline
      no-caps
      color="negative"
      icon="logout"
      label="Sair"
      class="full-width q-mt-lg"
      @click="sair"
    />

    <q-dialog v-model="dialogSenha">
      <q-card style="width: 100%; max-width: 400px;">
        <q-card-section class="text-h6">Alterar senha</q-card-section>
        <q-card-section class="q-gutter-md">
          <q-input
            v-model="senhaAtual"
            label="Senha atual"
            type="password"
            outlined
            bg-color="white"
          />
          <q-input
            v-model="senhaNova"
            label="Nova senha"
            :type="verNova ? 'text' : 'password'"
            outlined
            bg-color="white"
            hint="Mínimo de 8 caracteres"
          >
            <template #append>
              <q-icon
                :name="verNova ? 'visibility' : 'visibility_off'"
                class="cursor-pointer"
                @click="verNova = !verNova"
              />
            </template>
          </q-input>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat no-caps label="Cancelar" color="grey" v-close-popup />
          <q-btn unelevated no-caps label="Salvar" color="primary" :loading="salvando" @click="salvarSenha" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from '@/stores/auth-store'

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()

const dialogSenha = ref(false)
const salvando = ref(false)

const senhaAtual = ref('')
const senhaNova = ref('')
const verNova = ref(false)

function msgErro(err, fallback) {
  const d = err.response?.data?.detail
  if (Array.isArray(d)) return d.map((e) => e.msg).join(', ')
  return d || fallback
}

function abrirSenha() {
  senhaAtual.value = ''
  senhaNova.value = ''
  dialogSenha.value = true
}

async function salvarSenha() {
  if (!senhaAtual.value) {
    $q.notify({ type: 'negative', message: 'Informe a senha atual.' })
    return
  }
  if (senhaNova.value.length < 8) {
    $q.notify({ type: 'negative', message: 'A nova senha deve ter no mínimo 8 caracteres.' })
    return
  }
  salvando.value = true
  try {
    await authStore.alterarSenha(senhaAtual.value, senhaNova.value)
    $q.notify({ type: 'positive', message: 'Senha alterada.' })
    dialogSenha.value = false
  } catch (err) {
    $q.notify({ type: 'negative', message: msgErro(err, 'Erro ao alterar a senha.') })
  } finally {
    salvando.value = false
  }
}

function sair() {
  authStore.sair()
  router.push('/login')
}
</script>
