# 🤖 RPA - Monitor de Concursos do Amazonas

Este projeto consiste em um robô de automação (RPA - Robotic Process Automation) desenvolvido em Python, capaz de acessar automaticamente o site PCI Concursos, identificar concursos públicos no estado do Amazonas e organizar todas as informações relevantes de forma automatizada.

O sistema simula o comportamento de um usuário humano, navega pelas páginas, coleta dados, baixa editais e gera relatórios estruturados.

---

## 📌 Objetivo

Automatizar o processo de busca, coleta e organização de informações sobre concursos públicos, facilitando o acompanhamento de oportunidades e reduzindo tarefas manuais repetitivas.

---

## ⚙️ Funcionalidades

- Acessa automaticamente o site de concursos da região Norte  
- Filtra concursos do estado do Amazonas (AM)  
- Coleta:
  - Nome do concurso  
  - Faixa salarial  
  - Cargos disponíveis  
  - Data final de inscrição  
  - Link do concurso  
- Classifica concursos como:
  - URGENTE (até 3 dias para encerramento)  
  - NÃO URGENTE  
- Acessa cada concurso individualmente  
- Baixa automaticamente o edital em PDF (quando disponível)  
- Gera uma planilha Excel com os dados  
- Envia resumo via Telegram  

---

## 🧠 Tecnologias Utilizadas

- Python  
- Playwright (automação web)  
- Pandas (manipulação de dados)  
- Requests (requisições HTTP)  
- Openpyxl (geração de Excel)  

---

## 📂 Estrutura do Projeto

📁 Projeto_RPA_Bot_alerta_concursos  
│-- bot.py  
│-- requirements.txt  
│-- README.md  
│-- concursos_amazonas.xlsx  
│-- 📁 editais/  

---

## 💻 Pré-requisitos

Antes de executar o projeto, você precisa ter instalado:

- Python 3.10 ou superior  
- Git (opcional, para clonar o projeto)  

---

## 🚀 Passo a Passo de Execução

### 🔹 1. Baixar o projeto

Opção A - Via GitHub:

```bash
git clone https://github.com/Murilo344/Projeto_RPA_Bot_alerta_concursos.git
cd Projeto_RPA_Bot_alerta_concursos
