<template>
  <q-dialog v-model="aberto" persistent>
    <q-card style="width: 100%; max-width: 320px;" class="text-center q-pa-md">
      <q-card-section>
        <q-icon name="mic" size="56px" color="primary" />
        <div class="q-mt-sm">{{ gravando ? 'Gravando...' : 'Preparando...' }}</div>
      </q-card-section>
      <q-card-actions align="center">
        <q-btn flat no-caps label="Cancelar" color="grey" @click="cancelar" />
        <q-btn unelevated no-caps label="Parar" color="primary" :disable="!gravando" @click="parar" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useQuasar } from 'quasar'

const props = defineProps({ modelValue: Boolean })
const emit = defineEmits(['update:modelValue', 'gravado'])

const aberto = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v),
})

const $q = useQuasar()
const gravando = ref(false)
let gravador = null
let partes = []

watch(aberto, (v) => {
  if (v) {
    iniciar()
  }
})

async function iniciar() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    partes = []
    gravador = new MediaRecorder(stream)
    gravador.ondataavailable = (e) => partes.push(e.data)
    gravador.onstop = () => {
      stream.getTracks().forEach((t) => t.stop())
      const audio = new Blob(partes, { type: 'audio/webm' })
      emit('gravado', audio)
    }
    gravador.start()
    gravando.value = true
  } catch {
    $q.notify({ type: 'negative', message: 'Não foi possível acessar o microfone.' })
    aberto.value = false
  }
}

function parar() {
  if (gravador && gravando.value) {
    gravando.value = false
    gravador.stop()
  }
  aberto.value = false
}

function cancelar() {
  if (gravador && gravando.value) {
    gravador.onstop = null
    gravando.value = false
    gravador.stop()
  }
  aberto.value = false
}
</script>
