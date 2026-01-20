# 🔐 GUIA DO PAINEL ADMINISTRATIVO

## Como Acessar o Admin

### 1️⃣ Com o servidor rodando

Certifique-se que o servidor está ativo:
```bash
source venv/bin/activate  # Ativar ambiente virtual
python app.py             # Iniciar servidor
```

### 2️⃣ Acessar a URL do Admin

No navegador, acesse:
```
http://localhost:5000/admin
```

Ou se estiver acessando de outro dispositivo na rede:
```
http://SEU_IP:5000/admin
```

---

## 📊 O Que Você Encontra no Admin

### ABA 1: RESERVAS 📅

**O que mostra:**
- Todas as solicitações de reserva enviadas pelos clientes
- Nome, email, telefone, data desejada, número de pessoas
- Mensagens opcionais dos clientes
- Data/hora que a reserva foi recebida

**Como usar:**
1. Acesse a aba "Reservas"
2. Veja a tabela com todas as solicitações
3. Entre em contato com os clientes para confirmar
4. As reservas ficam salvas em `data/bookings.json`

💡 **Dica**: Você pode exportar esses dados para uma planilha se precisar!

---

### ABA 2: DEPOIMENTOS ⭐

**O que você pode fazer:**
- Adicionar novos depoimentos de clientes
- Ver todos os depoimentos existentes
- Escolher avaliação (3 a 5 estrelas)

**Como adicionar um depoimento:**
1. Clique na aba "Depoimentos"
2. Preencha o formulário:
   - Nome do cliente
   - Avaliação (estrelas)
   - Texto do depoimento
3. Clique em "Adicionar Depoimento"
4. O depoimento aparece automaticamente na página inicial!

**Exemplo de depoimento:**
```
Nome: Maria Silva
Avaliação: 5 Estrelas
Texto: "Experiência incrível! As estrelas, as histórias sobre 
UFOs e as fotos ficaram maravilhosas. Recomendo muito!"
```

---

### ABA 3: GALERIA 📸

**O que você pode fazer:**
- Adicionar fotos e vídeos à galeria
- Ver todos os itens publicados
- Cada item tem título e descrição

**Como adicionar à galeria:**
1. Clique na aba "Galeria"
2. Preencha o formulário:
   - **Título**: Nome da foto/vídeo
   - **Tipo**: Escolha "Imagem" ou "Vídeo"
   - **URL**: Link da imagem/vídeo
   - **Descrição**: Texto opcional sobre a foto
3. Clique em "Adicionar à Galeria"

**De onde pegar URLs de imagens:**

**Opção A: Upload no Imgur (Recomendado - Grátis)**
1. Acesse https://imgur.com
2. Faça upload da sua foto
3. Clique com botão direito na imagem → "Copiar endereço da imagem"
4. Cole no campo URL

**Opção B: Google Drive**
1. Faça upload no Google Drive
2. Compartilhe a imagem (deixe público)
3. Use um conversor de link do Drive
4. Cole a URL no formulário

**Opção C: Unsplash (fotos de exemplo)**
1. Acesse https://unsplash.com
2. Procure fotos de estrelas, chapada, etc.
3. Clique direito → "Copiar endereço da imagem"
4. Cole no formulário

**Exemplo de item da galeria:**
```
Título: Céu Estrelado na Chapada
Tipo: Imagem
URL: https://i.imgur.com/abc123.jpg
Descrição: Via Láctea sobre o Vale da Lua
```

---

## 🔒 SEGURANÇA IMPORTANTE

⚠️ **ATENÇÃO**: Este painel admin **NÃO TEM SENHA** por padrão!

Isso significa que qualquer pessoa que acessar `/admin` consegue ver e adicionar dados.

### Para proteger o admin em PRODUÇÃO:

**Opção 1: Adicionar autenticação básica (Simples)**

Edite o arquivo `app.py` e adicione antes das rotas:

```python
from functools import wraps
from flask import request, Response

def check_auth(username, password):
    return username == 'admin' and password == 'suasenha123'

def authenticate():
    return Response(
        'Login necessário', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# Depois, adicione @requires_auth antes das rotas admin:
@app.route('/admin')
@requires_auth
def admin():
    # código existente...
```

**Opção 2: Usar Flask-Login (Profissional)**
- Mais seguro e completo
- Requer mais configuração
- Recomendado para produção

**Opção 3: Restringir por IP**
- Permitir acesso apenas do seu IP
- Configurar no servidor/firewall

---

## 📂 Onde os Dados São Salvos

Todos os dados ficam na pasta `data/`:

```
chapada_tour/
└── data/
    ├── bookings.json       ← Reservas
    ├── testimonials.json   ← Depoimentos
    └── gallery.json        ← Galeria
```

### Fazendo Backup

**Backup manual:**
```bash
# Copiar toda a pasta data
cp -r data/ backup_data_$(date +%Y%m%d)/
```

**Backup automático (cron):**
```bash
# Editar crontab
crontab -e

# Adicionar linha (backup diário às 23h)
0 23 * * * cp -r /caminho/para/chapada_tour/data /caminho/para/backups/data_$(date +\%Y\%m\%d)
```

### Restaurando Backup

```bash
# Se perder os dados, restaure do backup
cp -r backup_data_20250117/data/ ./data/
```

---

## 📊 Exportando Dados

### Reservas para Excel/CSV

Os dados em JSON podem ser convertidos facilmente:

**Opção 1: Online**
1. Copie o conteúdo de `data/bookings.json`
2. Acesse https://www.convertcsv.com/json-to-csv.htm
3. Cole o JSON e converta para CSV
4. Abra no Excel

**Opção 2: Python script**
Crie um arquivo `export_reservas.py`:

```python
import json
import csv

with open('data/bookings.json', 'r', encoding='utf-8') as f:
    bookings = json.load(f)

with open('reservas.csv', 'w', encoding='utf-8', newline='') as f:
    if bookings:
        writer = csv.DictWriter(f, fieldnames=bookings[0].keys())
        writer.writeheader()
        writer.writerows(bookings)

print("Exportado para reservas.csv!")
```

Execute:
```bash
source venv/bin/activate
python export_reservas.py
```

---

## 🔄 Atualizando Conteúdo

### Editando dados manualmente (avançado)

Você pode editar os arquivos JSON diretamente:

```bash
nano data/testimonials.json
```

**Formato do JSON de depoimentos:**
```json
[
  {
    "id": 1,
    "name": "João Silva",
    "text": "Experiência incrível!",
    "rating": 5,
    "date": "17/01/2025"
  }
]
```

⚠️ **Cuidado**: Erros de sintaxe podem quebrar o site!

---

## 📱 Acessando de Celular/Tablet

1. Descubra o IP do seu computador Ubuntu:
```bash
hostname -I
```

2. No celular/tablet, acesse:
```
http://SEU_IP:5000/admin
```

3. Se não funcionar, libere a porta no firewall:
```bash
sudo ufw allow 5000
```

---

## ❓ Perguntas Frequentes

**P: Posso deletar reservas/depoimentos?**
R: Atualmente não há botão de deletar na interface. Você pode editar manualmente os arquivos JSON ou adicionar essa funcionalidade no código.

**P: As fotos da galeria ficam no meu servidor?**
R: Não! Você usa URLs externas (Imgur, etc). As imagens ficam hospedadas lá, o seu site apenas mostra.

**P: Posso ter múltiplos admins?**
R: Sim, mas você precisa implementar um sistema de login. Veja a seção de segurança.

**P: Os dados sobrevivem se eu parar o servidor?**
R: Sim! Tudo fica salvo em JSON mesmo quando o servidor está parado.

**P: Como recebo notificação de novas reservas?**
R: Atualmente não tem. Você precisa verificar o admin regularmente ou implementar envio de email (requer configuração adicional).

---

## 🚀 Melhorias Futuras Sugeridas

Para deixar o admin ainda melhor:

1. **Sistema de login/senha**
2. **Notificações por email de novas reservas**
3. **Botão para deletar itens**
4. **Editar itens existentes**
5. **Dashboard com estatísticas**
6. **Upload direto de imagens**
7. **Calendário de disponibilidade**
8. **Status de reservas (pendente/confirmada/cancelada)**

Se precisar dessas funcionalidades, posso te ajudar a implementar!

---

## 📞 Fluxo de Trabalho Recomendado

### Rotina Diária:
1. ✅ Acessar `/admin` pela manhã
2. ✅ Verificar novas reservas
3. ✅ Responder clientes por WhatsApp/Email
4. ✅ Adicionar fotos de passeios realizados
5. ✅ Pedir depoimentos aos clientes satisfeitos

### Rotina Semanal:
1. ✅ Fazer backup da pasta `data/`
2. ✅ Revisar depoimentos publicados
3. ✅ Atualizar galeria com melhores fotos
4. ✅ Verificar informações de contato atualizadas

---

**💡 Dica Final**: Marque `/admin` nos favoritos do navegador para acesso rápido!

🌟 **Qualquer dúvida, é só perguntar!** 🌟
