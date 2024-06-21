# Azure DevOps Updater

Este projeto fornece um script em Python para atualizar automaticamente o total de horas estimadas em um item de trabalho do Azure DevOps, somando as horas dos itens filhos e propagando a atualização para toda a árvore de itens.

## Requisitos

- Python 3.12.2
- pip

## Instalação

1. **Clone o repositório:**

   ```sh
   git clone https://github.com/felipehenrique159/script_atualiza_esforco_azure.git
   cd seu-repositorio
   ```

2. **Crie e ative um ambiente virtual:**

   ```sh
   python -m venv env
   source env/bin/activate  # Para sistemas Unix/Linux
   env\Scripts\activate  # Para Windows
   ```

3. **Instale as dependências:**

   ```sh
   pip install -r requirements.txt
   ```

## Configuração

Edite o arquivo `main.py` para incluir suas configurações específicas:

   ```python
   from azure_devops_updater import AzureDevOpsUpdater

   # Configurações
   organization_url = 'https://dev.azure.com/YOUR_ORG'
   pat_token = 'YOUR_PAT_TOKEN'
   project_name = 'YOUR_PROJECT_NAME'

   # Exemplo de uso
   updater = AzureDevOpsUpdater(organization_url, pat_token, project_name)
   updater.process_tree(root_work_item_id=12345)
   ```

Substitua `YOUR_ORG`, `YOUR_PAT_TOKEN`, `YOUR_PROJECT_NAME` e `12345` com os valores apropriados.

## Uso

Execute o script `main.py` para iniciar o processo de atualização:

   ```sh
   python main.py
   ```

## Estrutura do Projeto

```
seu_projeto/
│
├── azure_devops_updater.py  # Contém a classe AzureDevOpsUpdater
├── main.py                  # Script principal para executar a atualização
└── requirements.txt         # Lista de dependências do projeto
```
