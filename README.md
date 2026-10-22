# 💱 Conversor de Moedas

Um aplicativo desktop moderno de conversão de moedas com uma interface gráfica inspirada no Google Finance, desenvolvido em Python utilizando **CustomTkinter** e integrado com cotações em tempo real.

---

## Interface da aplicação 
A imagem abaixo apresenta a tela principal do sistema 

![Tela principal](imagens\tela_inicial.png)


## 🚀 Funcionalidades

* **Cotações em Tempo Real:** Consulta taxas de câmbio atualizadas diretamente da API pública da AwesomeAPI.
* **Conversão Bidirecional:** Permite digitar tanto o valor em Reais (BRL) para converter em moeda estrangeira, quanto o inverso.
* **Múltiplas Moedas:** Suporte nativo para as principais moedas globais e regionais:
  * Dólar Americano (`USD`)
  * Euro (`EUR`)
  * Libra Esterlina (`GBP`)
  * Peso Argentino (`ARS`)
* **Validação Robusta:** Tratamento de entradas inválidas, verificação de valores maiores que zero e tratamento de falhas de conexão com a API.

---

## 📂 Estrutura do Projeto

O projeto está dividido de forma modular para separar a interface gráfica da lógica de negócios:

* **`app.py`**: Responsável pela construção da interface gráfica com `CustomTkinter`, gerenciamento de abas de seleção de moedas, eventos de digitação em tempo real e atualização dos elementos visuais.
* **`backend.py`**: Concentra a lógica de conversão, requisições HTTP para a API (`requests`), normalização de códigos de moedas e validação de dados.

---

## 🛠️ Tecnologias Utilizadas

* **[Python](https://www.python.org/)**
* **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** (Interface Gráfica)
* **[Requests](https://requests.readthedocs.io/)** (Requisições HTTP)
* **[AwesomeAPI](https://docs.awesomeapi.com.br/)** (API de Cotações)

---

## ⚙️ Como Instalar e Executar

### Pré-requisitos
Certifique-se de ter o Python instalado em sua máquina.

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/nome-do-seu-repositorio.git](https://github.com/seu-usuario/nome-do-seu-repositorio.git)
   cd nome-do-seu-repositorio