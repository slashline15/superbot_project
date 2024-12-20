## Documentação do Projeto Superbot

Este documento descreve o projeto Superbot, um sistema automatizado para auxiliar engenheiros civis, simplificando processos e resolvendo problemas técnicos e gerenciais por meio de automação. O projeto integra um bot do Telegram, um banco de dados SQLite, e planeja integrar com o Notion e o N8n.

### 1. Arquitetura do Projeto

O projeto é estruturado em módulos para facilitar a organização e manutenção:

```
superbot_project/
├── scripts/
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── commands.py
│   │   ├── database.py
│   │   └── handlers.py
│   └── main_bot.py
├── superbot.db
└── .env
```

- **scripts/bot/**: Contém os módulos do bot do Telegram.
    - **__init__.py**: Arquivo vazio que define o diretório como um pacote Python.
    - **commands.py**: Funções dos comandos do bot (ex: /start, /notas).
    - **database.py**: Funções para conexão e manipulação do banco de dados.
    - **handlers.py**: Handlers para o `ConversationHandler` do bot, gerenciando o fluxo de conversa com o usuário.
- **scripts/main_bot.py**: Script principal que inicia o bot do Telegram.
- **superbot.db**: Arquivo do banco de dados SQLite.
- **.env**: Arquivo que armazena variáveis de ambiente, como tokens de API.

### 2. Configuração do Ambiente

**Pré-requisitos:**

- Python 3.9 ou superior.
- Git.
- Bibliotecas Python: `python-telegram-bot`, `notion-client`, `python-dotenv`, `sqlite3`.

**Passos:**

1. Clonar o Repositório:
   ```bash
   git clone https://github.com/slashline15/superbot_project.git
   ```

2. Criar e Ativar o Ambiente Virtual (recomendado):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  (Windows)
   source .venv/bin/activate (Linux/macOS)
   ```

3. Instalar Dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar o arquivo `.env`:
    ```
    TELEGRAM_API_KEY=seu_token_do_telegram
    NOTION_API_KEY=seu_token_do_notion
    ```

5. Criar o Banco de Dados:
   ```bash
   python scripts/setup_database.py
   ```

### 3. Bot do Telegram

O bot interage com os usuários via Telegram e registra as interações no banco de dados.

**Funcionalidades:**

- **/start**: Registra o usuário no banco de dados.
- Responder a mensagens de texto: Registra a mensagem no banco de dados e ecoa a mensagem de volta ao usuário.
- **/notas**: Lista as notas fiscais registradas no banco de dados.
- **/addnota**: Inicia uma conversa para registrar uma nova nota fiscal. Solicita ao usuário:  ID da obra, número da nota, valor, data de emissão e descrição.

**Como Executar:**

```bash
cd scripts
python main_bot.py
```

### 4. Banco de Dados (SQLite)

O banco de dados `superbot.db` armazena informações sobre usuários, mensagens, obras, insumos, pedidos, notas fiscais, fornecedores e prestadores de serviço.

**Tabelas:**

- **users**: Armazena informações dos usuários do Telegram.
- **message**: Armazena as mensagens trocadas com o bot.
- **files**: Armazena informações sobre arquivos (ainda não implementado).
- **obra**: Armazena informações sobre as obras.
- **tabela_insumos**: Armazena informações sobre insumos de cada obra.
- **meta**: Armazena metas relacionadas aos insumos das obras.
- **pedidos_de_compra**: Armazena informações sobre pedidos de compra.
- **pedidos_filhotes**: Armazena informações sobre pedidos filhos (relacionados a um pedido pai).
- **notas_fiscais**: Armazena informações sobre notas fiscais.
- **fornecedores**: Armazena informações sobre fornecedores.
- **prestadores_servico**: Armazena informações sobre prestadores de serviço.
- **medicao**: Armazena informações sobre medições realizadas por prestadores de serviço.

**(Verificar o código SQL no arquivo setup_database.py para detalhes das colunas e tipos de dados de cada tabela)**

### 5. Integração com Notion (Planejada)

Integração futura com o Notion para:

- Registrar dados do banco de dados.
- Criar páginas com informações específicas.

### 6. Integração com N8n (Planejada)

Integração futura com o N8n para automação de fluxos de trabalho, como:

- Gerar relatórios.
- Enviar notificações.

### 7. Fluxo de Trabalho com Git

- **Iniciar o trabalho:** `git pull origin main`
- **Salvar mudanças:** `git add .`, `git commit -m "Mensagem descritiva"`, `git push origin main`
- **Resolver conflitos:** `git merge origin/main --no-ff` ou `git rebase origin/main`

**Cuidados:**

- Manter o arquivo `.env` fora do controle de versão usando o `.gitignore`.
- Utilizar mensagens de commit claras e descritivas.

### 8. Próximos Passos

- Implementar a leitura de notas fiscais pelo bot.
- Desenvolver a geração de ficha de pagamento em PDF.
- Implementar o envio de PDF por email.
- Implementar as integrações com Notion e N8n.
- Criar mais comandos e funcionalidades para o bot.


### 9. Histórico de Problemas e Soluções

- **Problema:** Divergência de branches.
- **Solução:** `git pull origin main --no-ff`.

- **Problema:** Permissão negada ao `.gitignore`.
- **Solução:** Ajustar as permissões do arquivo usando `chmod 644 .gitignore` (Linux/macOS) ou via interface gráfica no Windows.

- **Problema:** Arquivos `.env` e `superbot.db` sendo rastreados pelo Git.
- **Solução:** Adicioná-los ao `.gitignore` e removê-los do cache do Git com `git rm --cached .env superbot.db`.

- **Problema:** Erro "no such table: users".
- **Solução:** Executar o script `scripts/setup_database.py` para criar as tabelas no banco de dados.

- **Problema:** Erro no `ConversationHandler` do comando /addnota.
- **Solução:** Mapear corretamente os estados do `ConversationHandler` e garantir que a função `cancelar` esteja definida.


### 10. Contato

Para dúvidas ou sugestões, entre em contato com o responsável pelo projeto.



Esta documentação será atualizada conforme o projeto evolui.