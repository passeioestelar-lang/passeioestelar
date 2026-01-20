# 🌌 Chapada Mística - Landing Page para Tour Turístico

Landing page moderna e visualmente impactante para divulgação de passeios turísticos na Chapada dos Veadeiros, com foco em ufologia, astronomia, cultura local e fotografia noturna.

## ✨ Características

- **Design Místico e Espacial**: Interface única com tema de estrelas e cosmos
- **Totalmente Responsivo**: Funciona perfeitamente em desktop, tablet e mobile
- **Animações Suaves**: Efeitos visuais que capturam a atenção
- **Sistema de Reservas**: Formulário para coleta de solicitações de reserva
- **Galeria Dinâmica**: Sistema para adicionar fotos e vídeos
- **Depoimentos**: Área para exibir feedbacks de clientes
- **Painel Admin**: Interface simples para gerenciar conteúdo

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos para rodar localmente:

1. **Clone ou baixe o projeto**

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação:**
```bash
python app.py
```

4. **Acesse no navegador:**
```
http://localhost:5000
```

## 📁 Estrutura do Projeto

```
chapada_tour/
├── app.py                  # Aplicação Flask principal
├── requirements.txt        # Dependências Python
├── data/                   # Dados em JSON (gerado automaticamente)
│   ├── bookings.json       # Reservas
│   ├── testimonials.json   # Depoimentos
│   └── gallery.json        # Galeria
├── static/
│   ├── css/
│   │   └── style.css       # Estilos principais
│   └── js/
│       └── script.js       # JavaScript interativo
└── templates/              # Templates HTML
    ├── base.html           # Template base
    ├── index.html          # Página inicial
    ├── about.html          # Sobre o passeio
    ├── gallery.html        # Galeria
    ├── booking.html        # Reservas
    └── admin.html          # Painel admin
```

## 🎨 Personalização

### Cores e Tema

Edite as variáveis CSS em `static/css/style.css`:

```css
:root {
    --color-space: #0a0e27;          /* Fundo principal */
    --color-accent: #00d4ff;         /* Cor de destaque */
    --color-accent-bright: #7c4dff;  /* Cor secundária */
    --color-star: #ffd700;           /* Cor dourada */
    /* ... outras cores */
}
```

### Fontes

O projeto usa:
- **Orbitron**: Para títulos e elementos display (tema espacial)
- **Crimson Text**: Para textos de corpo (elegância e legibilidade)

Para trocar, edite o link do Google Fonts em `templates/base.html`.

### Conteúdo Inicial

Os dados de exemplo são criados automaticamente na primeira execução. Para personalizar:

1. Edite os dados iniciais em `app.py` (linhas 91-113)
2. Ou use o painel admin em `/admin` para adicionar novos itens

### Informações de Contato

Atualize os dados de contato no rodapé em `templates/base.html`:

```html
<p class="footer-text">seu-email@exemplo.com</p>
<p class="footer-text">+55 (00) 0 0000-0000</p>
```

## 📊 Painel Administrativo

Acesse `/admin` para:
- Visualizar reservas recebidas
- Adicionar novos depoimentos
- Adicionar fotos/vídeos à galeria

**Nota**: Este é um painel básico sem autenticação. Para produção, adicione sistema de login.

## 🔧 Funcionalidades Futuras (Sugestões)

- [ ] Sistema de autenticação para admin
- [ ] Integração com banco de dados real (PostgreSQL, MySQL)
- [ ] Upload de imagens direto pelo admin
- [ ] Sistema de pagamento online
- [ ] Envio de emails automáticos para confirmação
- [ ] Calendário de disponibilidade
- [ ] Blog para compartilhar histórias
- [ ] Integração com redes sociais
- [ ] Sistema de avaliações verificadas
- [ ] Multilíngue (PT/EN/ES)

## 📱 Redes Sociais

Atualize os links das redes sociais em `templates/base.html`:

```html
<div class="footer-social">
    <a href="https://instagram.com/seu_perfil" class="social-link">Instagram</a>
    <a href="https://facebook.com/sua_pagina" class="social-link">Facebook</a>
    <a href="https://wa.me/5562999999999" class="social-link">WhatsApp</a>
</div>
```

## 🌐 Deploy (Produção)

Para colocar online, você pode usar:

### Opção 1: Heroku
```bash
# Crie um arquivo Procfile:
web: python app.py

# Configure o app.run() no final de app.py:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

### Opção 2: PythonAnywhere
1. Faça upload dos arquivos
2. Configure um Web App Flask
3. Aponte para o arquivo app.py

### Opção 3: VPS (DigitalOcean, AWS, etc.)
Use Nginx + Gunicorn para servir a aplicação

## 💡 Dicas de Uso

1. **Atualize regularmente a galeria** com fotos reais dos passeios
2. **Peça depoimentos** aos clientes satisfeitos
3. **Mantenha as informações atualizadas** (preços, horários)
4. **Use imagens de alta qualidade** para melhores resultados
5. **Teste em diferentes dispositivos** antes de divulgar

## 🎯 SEO e Marketing

Para melhorar o alcance:
- Adicione meta tags apropriadas
- Use imagens otimizadas (comprimidas)
- Crie conteúdo de blog sobre a região
- Integre com Google Analytics
- Configure Google My Business

## 📞 Suporte

Para dúvidas ou melhorias, sinta-se à vontade para:
- Adicionar issues no repositório
- Enviar pull requests com melhorias
- Entrar em contato

## 📄 Licença

Este projeto é livre para uso pessoal e comercial.

---

**Desenvolvido com ❤️ para promover as maravilhas da Chapada dos Veadeiros**

🌟 Bons passeios! 🌟
