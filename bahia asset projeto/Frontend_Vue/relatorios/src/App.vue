<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5037/api/Relatorios'; 

const emolumentosMedios = ref([]);
const emolumentosTotais = ref([]);
const posicaoAtivos = ref([]);

const dataFiltro = ref(new Date().toISOString().split('T')[0]); 
const ativoFiltro = ref('');
const loading = ref(false);

async function buscarRelatorios() {
    loading.value = true;
    try {
        const respMedio = await axios.get(`${API_BASE_URL}/emolumentos/medio`);
        emolumentosMedios.value = respMedio.data;

        const respTotal = await axios.get(`${API_BASE_URL}/emolumentos/total`);
        emolumentosTotais.value = respTotal.data;

        const respPosicao = await axios.get(`${API_BASE_URL}/posicao`, {
            params: {
                dataFinal: dataFiltro.value,
                ativo: ativoFiltro.value || null 
            }
        });
        posicaoAtivos.value = respPosicao.data;

    } catch (error) {
        console.error("Erro ao buscar dados da API. Verifique se o backend C# está rodando.", error);
        emolumentosMedios.value = [];
        emolumentosTotais.value = [];
        posicaoAtivos.value = [];
    } finally {
        loading.value = false;
    }
}

onMounted(() => {
    buscarRelatorios();
});

function formatDate(dateString) {
    if (!dateString) return '';
    return new Date(dateString).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' });
}

// NOVA FUNÇÃO: Formata a string YYYY-MM-DD para DD/MM/AAAA
function formatDateForTitle(dateString) {
    if (!dateString) return '';
    // Converte de YYYY-MM-DD para o objeto Date, e formata para pt-BR
    const parts = dateString.split('-');
    const date = new Date(parts[0], parts[1] - 1, parts[2]);
    return date.toLocaleDateString('pt-BR');
}

function formatCurrency(value, decimalPlaces = 2) {
    if (value === null || value === undefined) {
        return 'R$ 0,00';
    }
    
    const formatter = new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL',
        minimumFractionDigits: decimalPlaces,
        maximumFractionDigits: decimalPlaces,
    });
    
    return formatter.format(value).replace(/\s/g, '');
}
</script>

<template>
    <div class="container">
        <header class="main-header">
            <h1>📈 Relatórios de Emolumentos e Posições</h1>
            <p class="source-info">Sistema Integrado Fullstack: Python → SQL Server → C# API → Vue.js</p>
        </header>

        <div class="filtros-container">
            <h2 class="sub-header">Consultar Posição e Saldo</h2>
            <div class="filtros-group">
                <div class="input-item">
                    <label for="dataFiltro">Data Final (Posição):</label>
                    <input type="date" id="dataFiltro" v-model="dataFiltro" @change="buscarRelatorios">
                </div>
                
                <div class="input-item">
                    <label for="ativoFiltro">Ativo (Opcional):</label>
                    <input type="text" id="ativoFiltro" v-model="ativoFiltro" @keyup.enter="buscarRelatorios" placeholder="Ex: PETR4">
                </div>
                
                <button class="btn-action" @click="buscarRelatorios" :disabled="loading">
                    <span v-if="loading">Carregando...</span>
                    <span v-else>Recarregar Relatórios</span>
                </button>
            </div>
        </div>
        
        <hr class="divider">

        <div class="relatorios-grid">
            
            <div class="tabela-card card-posicao">
                <h2 class="card-title">Posição Total Acumulada em {{ formatDateForTitle(dataFiltro) }}</h2>
                <table class="tabela-relatorio">
                    <thead>
                        <tr>
                            <th>Ativo</th>
                            <th>Posição Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in posicaoAtivos" :key="item.ativo">
                            <td>{{ item.ativo }}</td>
                            <td :class="{'negativo': item.posicaoTotal < 0}">{{ item.posicaoTotal }}</td>
                        </tr>
                        <tr v-if="posicaoAtivos.length === 0 && !loading">
                            <td colspan="2" class="sem-dados">Nenhuma posição encontrada.</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="coluna-emolumentos">
                
                <div class="tabela-card card-emolumento">
                    <h2 class="card-title">Emolumentos Totais por Dia</h2>
                    <table class="tabela-relatorio">
                        <thead>
                            <tr>
                                <th>Data</th>
                                <th>Total (R$)</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in emolumentosTotais" :key="item.data_Trade">
                                <td>{{ formatDate(item.data_Trade) }}</td>
                                <td>{{ formatCurrency(item.emolumentoTotal, 2) }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="tabela-card card-emolumento">
                    <h2 class="card-title">Emolumentos Médios por Ativo</h2>
                    <table class="tabela-relatorio">
                        <thead>
                            <tr>
                                <th>Ativo</th>
                                <th>Média (R$)</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in emolumentosMedios" :key="item.ativo">
                                <td>{{ item.ativo }}</td>
                                <td>{{ formatCurrency(item.emolumentoMedio, 3) }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* CORES: Vermelho Escuro (#C0392B), Cinza Grafite (#333), Fundo (#F9F9F9) */
.container { max-width: 1200px; margin: 0 auto; padding: 30px; font-family: 'Roboto', sans-serif; background-color: #f9f9f9; min-height: 100vh; }
.main-header { padding-bottom: 15px; border-bottom: 3px solid #C0392B; margin-bottom: 30px; }
h1 { color: #333; font-size: 2.2em; font-weight: 700; margin: 0; }
.source-info { font-style: italic; color: #666; font-size: 1em; margin-top: 5px; }

.filtros-container { background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); margin-bottom: 25px; }
.sub-header { color: #333; font-size: 1.3em; margin-bottom: 15px; border-bottom: 1px dashed #ccc; padding-bottom: 10px; }
.filtros-group { display: flex; gap: 20px; align-items: flex-end; }
.input-item label { display: block; margin-bottom: 5px; color: #555; font-size: 0.9em; }
.filtros-group input { padding: 10px; border: 1px solid #ddd; border-radius: 4px; width: 180px; }
.btn-action { background-color: #C0392B; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; transition: background-color 0.2s; font-weight: bold; }
.btn-action:hover:not(:disabled) { background-color: #A93226; }
.btn-action:disabled { background-color: #D3D3D3; cursor: not-allowed; }

.relatorios-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 30px; } 
.coluna-emolumentos { display: flex; flex-direction: column; gap: 30px; }

.tabela-card { background-color: white; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); padding: 20px; }
.card-title { color: #333; font-size: 1.2em; margin-bottom: 15px; }

.tabela-relatorio { width: 100%; border-collapse: collapse; }
.tabela-relatorio th, .tabela-relatorio td { border: 1px solid #e0e0e0; padding: 12px; text-align: left; }
.tabela-relatorio th { background-color: #333; color: white; font-weight: 600; text-transform: uppercase; font-size: 0.9em; }
.tabela-relatorio tr:nth-child(even) { background-color: #f7f7f7; }

.negativo { color: #C0392B; font-weight: 700; background-color: #FFF0F0; }
.sem-dados { text-align: center !important; font-style: italic; color: #777; padding: 20px !important; }

@media (max-width: 900px) {
    .relatorios-grid {
        grid-template-columns: 1fr; 
    }
}
</style>