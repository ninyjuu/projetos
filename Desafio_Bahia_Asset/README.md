# 🚀 DESAFIO FULLSTACK: RELATÓRIOS DE EMOLUMENTOS E POSIÇÕES

### 🎯 Objetivo

Aplicação Fullstack para exibir relatórios financeiros, cumprindo todos os requisitos e o diferencial do **Extra 1 (API C#)**.

---

### 🛠️ ARQUITETURA E TECNOLOGIAS

O projeto é baseado em uma arquitetura de 4 camadas:

| Camada | Tecnologia | Função no Projeto |
| :--- | :--- | :--- |
| **Ingestão/ETL** | **Python** (pandas/pyodbc) | Leitura do CSV e inserção no banco. |
| **Banco** | **SQL Server** | Armazenamento e execução da lógica de relatório (Stored Procedures). |
| **Backend (API)** | **C# (.NET 8)** + **Dapper** | **Ponte de Dados:** Cria endpoints REST para consultar as SPs do SQL. |
| **Frontend (UI)** | **Vue.js 3 (Vite)** + **Axios** | Interface responsiva com filtros de data/ativo e estilo diferenciado (vermelho/grafite). |

---

### 💡 DESTAQUES TÉCNICOS E SOLUÇÕES

1.  **Posição Acumulada:** A lógica de saldo é calculada na Stored Procedure (`sp_PosicaoPorAtivoEData`) usando o filtro de data (`Data_Trade <= @DataFinal`) para acumular todas as transações até a data informada, conforme a regra de negócio.
2.  **Integridade de Dados:** O script Python trata o `input.csv` corrigindo problemas de `encoding` (BOM) e convertendo a vírgula decimal (`40,98`) para o ponto decimal (`40.98`), crucial para o SQL Server.
3.  **UI/UX:** A interface utiliza o esquema de cores Vermelho/Grafite (substituindo o azul padrão) e um layout Flexbox/Grid para ser visualmente distinto e profissional.
4.  **CORS:** A política `AllowAnyOrigin()` foi configurada no `Program.cs` do C# para permitir a comunicação com o Frontend Vue.js (rodando em porta diferente).

---

### ⚙️ INSTRUÇÕES DE EXECUÇÃO

O projeto deve ser iniciado em 3 terminais, na seguinte ordem:

#### 1. FASE DE SETUP (Apenas na Primeira Execução)

1.  **Criar Estrutura SQL:** Conecte-se ao SQL Server (`DBDesafioFullstack`) e execute o script **`Setup/stored_procedures_relatorios.sql`**.
2.  **Popular o Banco:** Navegue para a pasta `Setup` e execute:
    ```bash
    cd Setup
    python ingestao_dados.py
    ```

#### 2. INICIAR BACKEND (API C#)

1.  **Navegue para:** `cd Backend/AssetReportingAPI`
2.  **Execute o Servidor:**
    ```bash
    dotnet run
    ```
    *(Mantenha este terminal aberto. A API inicia em http://localhost:5037)*

#### 3. INICIAR FRONTEND (Vue.js)

1.  **Abra um novo terminal** e navegue para: `cd Frontend/relatorios`
2.  **Instale as dependências (Primeira vez):** `npm install`
3.  **Execute a Aplicação:**
    ```bash
    npm run dev
    ```

#### 🌐 ACESSO

Acesse a aplicação no navegador em: **`http://localhost:5173`**