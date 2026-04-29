from flask import Flask, render_template, request, redirect, url_for, session, flash
from GestorTareas import GestorTareas

app = Flask(__name__)
app.secret_key = '12345678'

gestor = GestorTareas()

# Crear usuario de prueba (coméntalo después)
gestor.crear_usuario("trevi", "juan@gmail.com", "1234")

@app.route('/')
def index():
    return redirect(url_for('inicio'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not first_name or not last_name or not email or not password:
            flash('Todos los campos son obligatorios')
            return redirect(url_for('registro'))
        
        if gestor.usuarios.find_one({"email": email}):
            flash('El correo ya está registrado')
            return redirect(url_for('registro'))
        
        nombre_completo = f"{first_name} {last_name}"
        gestor.usuarios.insert_one({
            "nombre": nombre_completo,
            "email": email,
            "password": password
        })
        
        flash('Registro exitoso. Ahora puedes iniciar sesión')
        return redirect(url_for('inicio'))
    
    return render_template('registro.html')

@app.route('/inicio', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Correo y contraseña son obligatorios')
            return redirect(url_for('inicio'))
        
        usuario = gestor.usuarios.find_one({"email": email})
        
        if usuario and usuario['password'] == password:
            session['user_id'] = str(usuario['_id'])
            session['user_nombre'] = usuario['nombre']
            flash('Inicio de sesión exitoso')
            return redirect(url_for('tareas'))
        else:
            flash('Correo o contraseña incorrectos')
            return redirect(url_for('inicio'))
    
    return render_template('inicio.html')

@app.route('/tareas')
def tareas():
    if 'user_id' not in session:
        flash('Debes iniciar sesión primero')
        return redirect(url_for('inicio'))
    return render_template('tareas.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada')
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True)