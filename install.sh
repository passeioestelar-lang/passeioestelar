#!/bin/bash

# Script de instalação automática para Ubuntu
# Chapada Mística - Landing Page

echo "🌌 Instalador Automático - Chapada Mística"
echo "=========================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para print colorido
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "ℹ $1"
}

# Verificar se está no diretório correto
if [ ! -f "app.py" ]; then
    print_error "Erro: Execute este script dentro da pasta 'chapada_tour'"
    exit 1
fi

print_info "Verificando instalação do Python..."

# Verificar se python3 está instalado
if ! command -v python3 &> /dev/null; then
    print_warning "Python3 não encontrado. Instalando..."
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
    print_success "Python3 instalado!"
else
    print_success "Python3 encontrado: $(python3 --version)"
fi

# Verificar se python3-venv está instalado
print_info "Verificando python3-venv..."
if ! dpkg -l | grep -q python3-venv; then
    print_warning "Instalando python3-venv..."
    sudo apt install -y python3-venv
fi
print_success "python3-venv disponível"

# Criar ambiente virtual
print_info "Criando ambiente virtual..."
if [ -d "venv" ]; then
    print_warning "Ambiente virtual já existe. Removendo o antigo..."
    rm -rf venv
fi

python3 -m venv venv
print_success "Ambiente virtual criado!"

# Ativar ambiente virtual
print_info "Ativando ambiente virtual..."
source venv/bin/activate

# Atualizar pip
print_info "Atualizando pip..."
pip install --upgrade pip > /dev/null 2>&1

# Instalar dependências
print_info "Instalando dependências do Flask..."
pip install -r requirements.txt
print_success "Dependências instaladas!"

# Criar diretório de dados
print_info "Configurando diretórios..."
mkdir -p data
print_success "Diretórios criados!"

echo ""
echo "=========================================="
print_success "Instalação concluída com sucesso!"
echo "=========================================="
echo ""
echo "📋 Para rodar o servidor:"
echo "   1. Ative o ambiente virtual:"
echo "      ${YELLOW}source venv/bin/activate${NC}"
echo ""
echo "   2. Execute o servidor:"
echo "      ${YELLOW}python app.py${NC}"
echo ""
echo "   3. Acesse no navegador:"
echo "      ${GREEN}http://localhost:5000${NC}"
echo ""
echo "💡 Dica: Para facilitar, use o script de início rápido:"
echo "   ${YELLOW}./start.sh${NC}"
echo ""

# Criar script de início rápido
print_info "Criando script de início rápido..."
cat > start.sh << 'EOF'
#!/bin/bash

# Script de início rápido
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "Execute primeiro: ./install.sh"
    exit 1
fi

echo "🌌 Iniciando Chapada Mística..."
source venv/bin/activate
python app.py
EOF

chmod +x start.sh
print_success "Script 'start.sh' criado!"

echo ""
print_info "Deseja iniciar o servidor agora? (s/n)"
read -r resposta

if [ "$resposta" = "s" ] || [ "$resposta" = "S" ]; then
    echo ""
    echo "🚀 Iniciando servidor..."
    echo "   Pressione Ctrl+C para parar"
    echo ""
    python app.py
else
    print_info "OK! Para iniciar depois, use: ./start.sh"
fi
