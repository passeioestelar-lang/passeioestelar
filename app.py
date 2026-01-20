from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import os
import json

app = Flask(__name__)
app.secret_key = 'chapada-veadeiros-secret-key-2025'

# Credenciais de admin (MUDE A SENHA!)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD_HASH = generate_password_hash('P@ssE10_E5t3l@r-26')  # MUDE ESTA SENHA!

# Configurações de upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'webm', 'mov', 'avi'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB para imagens
MAX_VIDEO_SIZE = 500 * 1024 * 1024  # 500MB para vídeos

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_VIDEO_SIZE

# Criar pasta de uploads se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'videos'), exist_ok=True)

# Diretório para dados (simulando banco de dados com JSON)
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_video(filename):
    """Verifica se a extensão do vídeo é permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

def load_data(filename):
    """Carrega dados de um arquivo JSON"""
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(filename, data):
    """Salva dados em um arquivo JSON"""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def login_required(f):
    """Decorator para proteger rotas que requerem login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Por favor, faça login para acessar esta página.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Página principal"""
    testimonials = load_data('testimonials.json')
    gallery = load_data('gallery.json')
    return render_template('index.html', testimonials=testimonials, gallery=gallery)

@app.route('/sobre')
def about():
    """Página sobre o passeio"""
    return render_template('about.html')

@app.route('/galeria')
def gallery():
    """Página de galeria"""
    gallery_items = load_data('gallery.json')
    return render_template('gallery.html', gallery=gallery_items)

@app.route('/experiencias')
def experiencias():
    """Página de experiências reais (vídeo depoimentos)"""
    video_testimonials = load_data('video_testimonials.json')
    return render_template('experiencias.html', videos=video_testimonials)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Página de login do admin"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['logged_in'] = True
            session['username'] = username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Usuário ou senha incorretos!', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """Faz logout do admin"""
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/reservar', methods=['GET', 'POST'])
def booking():
    """Página de reserva"""
    if request.method == 'POST':
        # Processa reserva
        booking_data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'date': request.form.get('date'),
            'people': request.form.get('people'),
            'message': request.form.get('message'),
            'timestamp': datetime.now().isoformat()
        }
        
        bookings = load_data('bookings.json')
        bookings.append(booking_data)
        save_data('bookings.json', bookings)
        
        flash('Reserva enviada com sucesso! Entraremos em contato em breve.', 'success')
        return redirect(url_for('index'))
    
    return render_template('booking.html')

@app.route('/admin')
@login_required
def admin():
    """Painel administrativo (básico)"""
    bookings = load_data('bookings.json')
    testimonials = load_data('testimonials.json')
    gallery_items = load_data('gallery.json')
    video_testimonials = load_data('video_testimonials.json')
    
    return render_template('admin.html', 
                         bookings=bookings, 
                         testimonials=testimonials,
                         gallery=gallery_items,
                         videos=video_testimonials)

@app.route('/admin/add-testimonial', methods=['POST'])
@login_required
def add_testimonial():
    """Adiciona depoimento"""
    testimonial = {
        'id': datetime.now().timestamp(),
        'name': request.form.get('name'),
        'text': request.form.get('text'),
        'rating': int(request.form.get('rating', 5)),
        'date': datetime.now().strftime('%d/%m/%Y')
    }
    
    testimonials = load_data('testimonials.json')
    testimonials.append(testimonial)
    save_data('testimonials.json', testimonials)
    
    flash('Depoimento adicionado!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/add-gallery', methods=['POST'])
@login_required
def add_gallery():
    """Adiciona item à galeria (upload de arquivo ou URL)"""
    try:
        item = {
            'id': datetime.now().timestamp(),
            'title': request.form.get('title'),
            'type': request.form.get('type', 'image'),
            'description': request.form.get('description', '')
        }
        
        # Verificar se é upload de arquivo ou URL
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            
            # Validar arquivo
            if not allowed_file(file.filename):
                flash('Tipo de arquivo não permitido! Use: PNG, JPG, JPEG, GIF, WEBP', 'error')
                return redirect(url_for('admin'))
            
            # Gerar nome seguro e único
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            
            # Salvar arquivo
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # URL relativa para o banco de dados
            item['url'] = url_for('static', filename=f'uploads/{filename}')
            item['uploaded'] = True
            
        elif request.form.get('url'):
            # Usar URL fornecida
            item['url'] = request.form.get('url')
            item['uploaded'] = False
        else:
            flash('Você deve fazer upload de uma imagem ou fornecer uma URL!', 'error')
            return redirect(url_for('admin'))
        
        # Adicionar à galeria
        gallery_items = load_data('gallery.json')
        gallery_items.append(item)
        save_data('gallery.json', gallery_items)
        
        flash('Item adicionado à galeria com sucesso!', 'success')
        
    except Exception as e:
        flash(f'Erro ao adicionar item: {str(e)}', 'error')
    
    return redirect(url_for('admin'))

@app.route('/admin/delete-gallery/<item_id>', methods=['POST'])
@login_required
def delete_gallery(item_id):
    """Deleta item da galeria"""
    try:
        gallery_items = load_data('gallery.json')
        item_id_float = float(item_id)
        
        # Encontrar e remover o item
        item_to_delete = None
        for item in gallery_items:
            if item['id'] == item_id_float:
                item_to_delete = item
                break
        
        if item_to_delete:
            # Se for upload local, deletar arquivo também
            if item_to_delete.get('uploaded', False):
                try:
                    # Extrair nome do arquivo da URL
                    filename = item_to_delete['url'].split('/')[-1]
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    if os.path.exists(filepath):
                        os.remove(filepath)
                except:
                    pass  # Se não conseguir deletar arquivo, continua
            
            # Remover do JSON
            gallery_items = [item for item in gallery_items if item['id'] != item_id_float]
            save_data('gallery.json', gallery_items)
            
            flash('Item removido da galeria!', 'success')
        else:
            flash('Item não encontrado!', 'error')
            
    except Exception as e:
        flash(f'Erro ao remover item: {str(e)}', 'error')
    
    return redirect(url_for('admin'))

@app.route('/admin/add-video', methods=['POST'])
@login_required
def add_video():
    """Adiciona vídeo depoimento"""
    try:
        video = {
            'id': datetime.now().timestamp(),
            'name': request.form.get('name'),
            'title': request.form.get('title'),
            'rating': int(request.form.get('rating', 5)),
            'date': datetime.now().strftime('%d/%m/%Y')
        }
        
        # Verificar se é upload de arquivo ou URL
        if 'video_file' in request.files and request.files['video_file'].filename != '':
            file = request.files['video_file']
            
            # Validar arquivo
            if not allowed_video(file.filename):
                flash('Tipo de vídeo não permitido! Use: MP4, WEBM, MOV, AVI', 'error')
                return redirect(url_for('admin'))
            
            # Gerar nome seguro e único
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            
            # Salvar arquivo na pasta videos
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'videos', filename)
            file.save(filepath)
            
            # URL relativa para o banco de dados
            video['url'] = url_for('static', filename=f'uploads/videos/{filename}')
            video['uploaded'] = True
            video['thumbnail'] = request.form.get('thumbnail', '')
            
        elif request.form.get('video_url'):
            # Usar URL fornecida (YouTube, Vimeo, etc)
            video['url'] = request.form.get('video_url')
            video['uploaded'] = False
            video['thumbnail'] = request.form.get('thumbnail', '')
        else:
            flash('Você deve fazer upload de um vídeo ou fornecer uma URL!', 'error')
            return redirect(url_for('admin'))
        
        # Adicionar aos vídeos
        videos = load_data('video_testimonials.json')
        videos.append(video)
        save_data('video_testimonials.json', videos)
        
        flash('Vídeo depoimento adicionado com sucesso!', 'success')
        
    except Exception as e:
        flash(f'Erro ao adicionar vídeo: {str(e)}', 'error')
    
    return redirect(url_for('admin'))

@app.route('/admin/delete-video/<video_id>', methods=['POST'])
@login_required
def delete_video(video_id):
    """Deleta vídeo depoimento"""
    try:
        videos = load_data('video_testimonials.json')
        video_id_float = float(video_id)
        
        # Encontrar e remover o vídeo
        video_to_delete = None
        for video in videos:
            if video['id'] == video_id_float:
                video_to_delete = video
                break
        
        if video_to_delete:
            # Se for upload local, deletar arquivo também
            if video_to_delete.get('uploaded', False):
                try:
                    filename = video_to_delete['url'].split('/')[-1]
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'videos', filename)
                    if os.path.exists(filepath):
                        os.remove(filepath)
                except:
                    pass
            
            # Remover do JSON
            videos = [v for v in videos if v['id'] != video_id_float]
            save_data('video_testimonials.json', videos)
            
            flash('Vídeo removido!', 'success')
        else:
            flash('Vídeo não encontrado!', 'error')
            
    except Exception as e:
        flash(f'Erro ao remover vídeo: {str(e)}', 'error')
    
    return redirect(url_for('admin'))

if __name__ == '__main__':
    # Inicializa dados de exemplo se não existirem
    if not os.path.exists(os.path.join(DATA_DIR, 'testimonials.json')):
        sample_testimonials = [
            {
                'id': 1,
                'name': 'Maria Silva',
                'text': 'Uma experiência inesquecível! Ver as estrelas na Chapada enquanto ouvíamos histórias sobre UFOs foi mágico.',
                'rating': 5,
                'date': '15/01/2025'
            },
            {
                'id': 2,
                'name': 'João Santos',
                'text': 'O guia é incrível! As fotos noturnas ficaram espetaculares e as histórias da região são fascinantes.',
                'rating': 5,
                'date': '10/01/2025'
            }
        ]
        save_data('testimonials.json', sample_testimonials)
    
    if not os.path.exists(os.path.join(DATA_DIR, 'gallery.json')):
        sample_gallery = [
            {
                'id': 1,
                'title': 'Céu Estrelado',
                'url': 'https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=800',
                'type': 'image',
                'description': 'Via Láctea sobre a Chapada'
            },
            {
                'id': 2,
                'title': 'Fotografia Noturna',
                'url': 'https://images.unsplash.com/photo-1502134249126-9f3755a50d78?w=800',
                'type': 'image',
                'description': 'Sessão de fotos com as estrelas'
            }
        ]
        save_data('gallery.json', sample_gallery)
    
    if not os.path.exists(os.path.join(DATA_DIR, 'video_testimonials.json')):
        sample_videos = []
        save_data('video_testimonials.json', sample_videos)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
