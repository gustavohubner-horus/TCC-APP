<template>
  <q-page class="q-pa-md">
    <q-card flat bordered class="q-mb-md">
      <q-card-section class="row items-center justify-between q-py-sm">
        <div class="text-subtitle1">Gastos deste mês</div>
        <div class="text-h6 text-primary">{{ formatar(totalMes) }}</div>
      </q-card-section>
    </q-card>

    <q-card v-if="porCategoria.length" flat bordered class="q-mb-md">
      <q-card-section>
        <div class="text-subtitle2 q-mb-sm">Por categoria</div>
        <apexchart type="pie" height="260" :options="pizzaOpcoes" :series="pizzaSeries" />
      </q-card-section>
    </q-card>

    <q-card flat bordered class="q-mb-md">
      <q-card-section>
        <div class="text-subtitle2 q-mb-sm">Gastos dos últimos 6 meses</div>
        <apexchart type="line" height="240" :options="linhaOpcoes" :series="linhaSeries" />
      </q-card-section>
    </q-card>

    <q-card v-if="limitesInfo.length" flat bordered>
      <q-card-section>
        <div class="text-subtitle2 q-mb-md">Uso dos limites</div>
        <div v-for="l in limitesInfo" :key="l.nome" class="q-mb-md">
          <div class="row items-center justify-between q-mb-xs">
            <span>{{ l.nome }}</span>
            <span class="text-caption text-grey-7">{{ valorCurto(l.gasto) }} / {{ valorCurto(l.limite) }}</span>
          </div>
          <q-linear-progress :value="Math.min(l.pct / 100, 1)" :color="corLimite(l.pct)" rounded size="10px" />
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useGastoStore } from '@/stores/gasto-store'
import { useCategoriaStore } from '@/stores/categoria-store'
import { useLimiteStore } from '@/stores/limite-store'

const gastoStore = useGastoStore()
const catStore = useCategoriaStore()
const limiteStore = useLimiteStore()

const cores = ['#15803D', '#26a69a', '#f2c037', '#31ccec', '#9c27b0', '#c10015', '#1976d2', '#ff7043']

onMounted(async () => {
  await catStore.carregarCategorias()
  await limiteStore.carregarLimites()
  await gastoStore.carregarGastos()
})

const gastosDoMes = computed(() => {
  const prefixo = new Date().toISOString().slice(0, 7)
  return gastoStore.gastos.filter((g) => g.gas_data.startsWith(prefixo))
})

const totalMes = computed(() =>
  gastosDoMes.value.reduce((soma, g) => soma + Number(g.gas_valor), 0),
)

const porCategoria = computed(() => {
  const lista = []
  for (const cat of catStore.categorias) {
    const total = gastosDoMes.value
      .filter((g) => g.cat_id === cat.cat_id)
      .reduce((soma, g) => soma + Number(g.gas_valor), 0)
    if (total > 0) {
      lista.push({ nome: cat.cat_nome, total })
    }
  }
  const semCategoria = gastosDoMes.value
    .filter((g) => !g.cat_id)
    .reduce((soma, g) => soma + Number(g.gas_valor), 0)
  if (semCategoria > 0) {
    lista.push({ nome: 'Sem categoria', total: semCategoria })
  }
  return lista
})

const ultimos6Meses = computed(() => {
  const meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
  const labels = []
  const valores = []
  const hoje = new Date()
  for (let i = 5; i >= 0; i--) {
    const d = new Date(hoje.getFullYear(), hoje.getMonth() - i, 1)
    const ano = d.getFullYear()
    const mes = String(d.getMonth() + 1).padStart(2, '0')
    const prefixo = `${ano}-${mes}`
    const total = gastoStore.gastos
      .filter((g) => g.gas_data.startsWith(prefixo))
      .reduce((soma, g) => soma + Number(g.gas_valor), 0)
    labels.push(meses[d.getMonth()])
    valores.push(total)
  }
  return { labels, valores }
})

const limitesInfo = computed(() => {
  const lista = []
  for (const cat of catStore.categorias) {
    const limite = limiteDe(cat.cat_id)
    if (!limite) continue
    const gasto = gastosDoMes.value
      .filter((g) => g.cat_id === cat.cat_id)
      .reduce((soma, g) => soma + Number(g.gas_valor), 0)
    lista.push({ nome: cat.cat_nome, gasto, limite, pct: Math.round((gasto / limite) * 100) })
  }
  return lista
})

const pizzaSeries = computed(() => porCategoria.value.map((c) => c.total))
const pizzaOpcoes = computed(() => ({
  labels: porCategoria.value.map((c) => `${c.nome} - ${formatar(c.total)}`),
  colors: cores,
  legend: { position: 'bottom' },
  tooltip: { y: { formatter: (v) => formatar(v) } },
}))

const linhaSeries = computed(() => [{ name: 'Gastos', data: ultimos6Meses.value.valores }])
const linhaOpcoes = computed(() => ({
  chart: { toolbar: { show: false } },
  colors: ['#15803D'],
  stroke: { curve: 'smooth' },
  dataLabels: { enabled: false },
  xaxis: { categories: ultimos6Meses.value.labels },
  yaxis: { labels: { formatter: (v) => formatar(v) } },
}))

function corLimite(pct) {
  if (pct > 100) return 'negative'
  if (pct >= 80) return 'orange'
  return 'primary'
}

function valorCurto(v) {
  return Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 })
}

function limiteDe(id) {
  if (!id) return null
  const l = limiteStore.limites.find((x) => x.cat_id === id)
  return l ? Number(l.lim_valor) : null
}

function formatar(v) {
  return Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}
</script>
