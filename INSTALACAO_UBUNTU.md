# 🐧 GUIA DE INSTALAÇÃO PARA UBUNTU

## ⚠️ IMPORTANTE: Use Ambiente Virtual (Recomendado)

O Ubuntu moderno requer uso de ambiente virtual para instalar pacotes Python.
Isso é mais seguro e profissional!

---

## 🚀 Instalação Passo a Passo

### 1️⃣ Instalar dependências do sistema
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### 2️⃣ Navegar até a pasta do projeto
```bash
cd /caminho/para/chapada_tour
```

### 3️⃣ Criar ambiente virtual
```bash
python3 -m venv venv
```

### 4️⃣ Ativar ambiente virtual
```bash
source venv/bin/activate
```
💡 Você verá `(venv)` no início da linha do terminal quando estiver ativo

### 5️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

### 6️⃣ Rodar o servidor
```bash
python app.py
```

🎉 Pronto! Acesse: http://localhost:5000

---

## 🔄 Para usar depois

### Sempre que for rodar o projeto:

1. **Ativar o ambiente virtual:**
```bash
cd /caminho/para/chapada_tour
source venv/bin/activate
```

2. **Rodar o servidor:**
```bash
python app.py
```

3. **Desativar quando terminar (opcional):**
```bash
deactivate
```

---

## 🆘 ALTERNATIVA RÁPIDA (Não recomendada)

Se você realmente precisa instalar globalmente:

```bash
pip install -r requirements.txt --break-system-packages
```

⚠️ **AVISO**: Isso pode causar conflitos no sistema. Use apenas para testes rápidos.

---

## 📁 Estrutura após instalação

```
chapada_tour/
├── venv/                    # ← Ambiente virtual (criado por você)
│   ├── bin/
│   ├── lib/
│   └── ...
├── app.py
├── requirements.txt
├── data/                    # ← Criado automaticamente ao rodar
├── static/
└── templates/
```

💡 O arquivo `.gitignore` já está configurado para ignorar a pasta `venv/`

---

## 🌐 Para deixar acessível na rede local

Por padrão, o Flask só aceita conexões do próprio computador.
Para acessar de outros dispositivos na mesma rede:

1. **Descubra seu IP local:**
```bash
ip addr show | grep inet
```
Procure por algo como `192.168.x.x`

2. **O servidor já está configurado para aceitar conexões externas**
(linha `host='0.0.0.0'` no app.py)

3. **Acesse de outro dispositivo:**
```
http://192.168.x.x:5000
```
(substitua pelo seu IP)

4. **Se não funcionar, libere a porta no firewall:**
```bash
sudo ufw allow 5000
```

---

## 🔧 Scripts úteis (opcional)

### Criar arquivo `start.sh` para facilitar:

```bash
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python app.py
```

Tornar executável:
```bash
chmod +x start.sh
```

Usar:
```bash
./start.sh
```

---

## 📦 Instalação de dependências adicionais (futuro)

Sempre com o ambiente virtual ativo:

```bash
source venv/bin/activate
pip install nome-do-pacote
pip freeze > requirements.txt  # Atualiza o arquivo
```

---

## 🐛 Problemas comuns

### "comando python não encontrado"
Use `python3` ao invés de `python`:
```bash
python3 -m venv venv
python3 app.py
```

### "Porta 5000 já em uso"
Edite `app.py` e mude a porta:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Troque 5000 por 8080
```

### Esqueceu de ativar o ambiente virtual
Se der erro de módulo não encontrado:
```bash
source venv/bin/activate
```

### Permissões negadas
```bash
sudo chown -R $USER:$USER .
```

---

## ✅ Checklist de instalação

- [ ] Instalei `python3-venv`
- [ ] Criei o ambiente virtual (`python3 -m venv venv`)
- [ ] Ativei o ambiente virtual (`source venv/bin/activate`)
- [ ] Instalei as dependências (`pip install -r requirements.txt`)
- [ ] Rodei o servidor (`python app.py`)
- [ ] Acessei http://localhost:5000 no navegador
- [ ] Funcionou! 🎉

---

## 🎓 Entendendo o ambiente virtual

**Por que usar?**
- Isola dependências do projeto
- Evita conflitos entre projetos diferentes
- É a prática profissional recomendada
- Facilita deploy em produção

**O que é o venv/?**
- Uma pasta com uma cópia isolada do Python
- Contém todas as bibliotecas do projeto
- Não afeta o Python do sistema

---

## 🚀 Próximos passos

Após instalar e testar:

1. Personalize as informações de contato
2. Adicione suas próprias fotos na galeria
3. Teste em diferentes navegadores
4. Configure para produção quando estiver pronto

---

**💚 Desenvolvido para Ubuntu | Testado em Ubuntu 22.04 e 24.04**
