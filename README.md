# Superbot Project

## Sobre o Projeto
Este projeto visa criar um sistema automatizado para engenheiros civis, simplificando tarefas técnicas e gerenciais por meio de automações e bots.

---

## Configuração do Repositório

### 1. Clonar o Repositório
Para começar a trabalhar com o projeto, clone o repositório:
```bash
git clone https://github.com/seu-usuario/superbot_project.git
```

## Contato

- Se precisar de ajuda, entre em contato com o responsável pelo projeto.

## Bot do Telegram

O bot do Telegram é responsável por interagir com os usuários e registrar suas mensagens no banco de dados SQLite. Ele foi projetado para:

- Responder ao comando `/start`, registrando o usuário no banco de dados.
- Responder a mensagens de texto e registrar as mensagens no banco de dados.
- Garantir que cada usuário seja registrado apenas uma vez.

### Como Iniciar o Bot

1. Certifique-se de ter o token do bot fornecido pelo [BotFather](https://t.me/botfather) e adicione-o ao arquivo `.env`:
TELEGRAM_API_KEY=seu_token_aqui


2. Execute o bot no terminal:
```bash
python scripts/telegram_bot.py
```
3. Interaja com o bot no Telegram:

Use `/start` para se registrar.
Envie mensagens para ver as respostas e registrar os textos no banco de dados

---

## Principais Funcionalidades
- Registrar Usuários: Quando um usuário envia o comando /start, suas informações são registradas no banco de dados, incluindo:
    - ID do usuário
    - Nome de usuário (se disponível)
    - Nome e sobrenome
- Registrar Mensagens: Toda mensagem de texto enviada ao bot é registrada no banco de dados com:
    - ID do usuário
    - Conteúdo da mensagem
    - Data e hora do envio


---

#### **2. Estrutura do Banco de Dados**
Inclua detalhes sobre as tabelas criadas no SQLite, explicando a finalidade de cada uma e suas colunas.

```markdown
## Estrutura do Banco de Dados SQLite

O banco de dados `superbot.db` contém duas tabelas principais: `usuarios` e `mensagens`.

### Tabela: `usuarios`
Armazena informações básicas dos usuários registrados no bot.

| Coluna       | Tipo     | Descrição                                        |
|--------------|----------|--------------------------------------------------|
| `id`         | INTEGER  | ID único do usuário no Telegram. Chave primária. |
| `username`   | TEXT     | Nome de usuário no Telegram (se disponível).     |
| `first_name` | TEXT     | Primeiro nome do usuário.                        |
| `last_name`  | TEXT     | Sobrenome do usuário (se disponível).            |

### Tabela: `mensagens`
Armazena todas as mensagens enviadas pelos usuários ao bot.

| Coluna       | Tipo     | Descrição                                                              |
|--------------|----------|------------------------------------------------------------------------|
| `id`         | INTEGER  | ID único da mensagem. Chave primária.                                  |
| `user_id`    | INTEGER  | ID do usuário que enviou a mensagem (relacionado à tabela `usuarios`). |
| `text`       | TEXT     | Conteúdo da mensagem enviada.                                          |
| `timestamp`  | DATETIME | Data e hora em que a mensagem foi enviada.                             |

---

### Relacionamento entre Tabelas

A tabela `mensagens` possui uma relação com a tabela `usuarios`, onde o campo `user_id` faz referência ao campo `id` da tabela `usuarios`. Isso garante que cada mensagem esteja associada a um usuário registrado.

---

## Cuidados e Boas Práticas

1. **Sincronização:**
   - Certifique-se de sincronizar o repositório antes de trabalhar no bot:
     ```bash
     git pull origin main
     ```

2. **Manutenção do Banco de Dados:**
   - Use ferramentas como [DB Browser for SQLite](https://sqlitebrowser.org/) para visualizar e gerenciar os dados do banco.
   - Realize backups regulares do arquivo `superbot.db`.

3. **Gerenciamento de Tokens:**
   - Nunca exponha o token do bot ou outras informações sensíveis. Garanta que o arquivo `.env` está listado no `.gitignore`:
     ```
     .env
     ```

4. **Testes:**
   - Teste o bot regularmente no ambiente de desenvolvimento antes de usar em produção.
   - Verifique se as tabelas do banco de dados estão funcionando corretamente com consultas simples:
     ```sql
     SELECT * FROM usuarios;
     SELECT * FROM mensagens;
     ```
---

## Próximos Passos

1. **Expandir Funcionalidades do Bot:**
   - Adicionar comando `/mensagens` para listar mensagens de um usuário.
   - Criar comando `/usuarios` para listar todos os usuários registrados.

2. **Automação:**
   - Integrar fluxos do bot com ferramentas como Notion e N8n.

3. **Melhorar a Documentação:**
   - Detalhar processos adicionais conforme o projeto evoluir.




