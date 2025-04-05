from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pymysql
from pymysql.cursors import DictCursor
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import config

app = Flask(__name__)
app.config.from_object(config.Config)

# Initialize MySQL connection with PyMySQL
def get_db_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        cursorclass=DictCursor
    )

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Loader
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, username FROM users WHERE id = %s", (user_id,))
            user_data = cur.fetchone()
            if user_data:
                return User(id=user_data['id'], username=user_data['username'])
            return None
    finally:
        conn.close()

# Routes
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('appointments'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM users WHERE username = %s", (username,))
                if cur.fetchone() is not None:
                    flash('Username already exists', 'danger')
                    return redirect(url_for('register'))
                
                hashed_password = generate_password_hash(password)
                cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                          (username, hashed_password))
                conn.commit()
                flash('Registration successful. Please login.', 'success')
                return redirect(url_for('login'))
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
                user_data = cur.fetchone()
                
                if user_data and check_password_hash(user_data['password'], password):
                    user = User(id=user_data['id'], username=user_data['username'])
                    login_user(user)
                    return redirect(url_for('appointments'))
                else:
                    flash('Invalid username or password', 'danger')
        finally:
            conn.close()
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/appointments')
@login_required
def appointments():
    status_filter = request.args.get('status', 'all')
    date_filter = request.args.get('date_range', 'all')
    sort_by = request.args.get('sort', 'date_asc')
    
    # Base query
    query = "SELECT * FROM appointments WHERE user_id = %s"
    params = [current_user.id]
    
    # Apply filters
    if status_filter != 'all':
        query += " AND status = %s"
        params.append(status_filter)
    
    if date_filter == 'today':
        today = datetime.now().date()
        query += " AND DATE(date_time) = %s"
        params.append(today)
    elif date_filter == 'week':
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        query += " AND DATE(date_time) BETWEEN %s AND %s"
        params.extend([today, next_week])
    elif date_filter == 'month':
        today = datetime.now().date()
        next_month = today + timedelta(days=30)
        query += " AND DATE(date_time) BETWEEN %s AND %s"
        params.extend([today, next_month])
    
    # Apply sorting
    if sort_by == 'date_asc':
        query += " ORDER BY date_time ASC"
    elif sort_by == 'date_desc':
        query += " ORDER BY date_time DESC"
    elif sort_by == 'provider_asc':
        query += " ORDER BY provider_name ASC"
    elif sort_by == 'provider_desc':
        query += " ORDER BY provider_name DESC"
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, tuple(params))
            appointments = cur.fetchall()
            
            # Get summary counts
            today = datetime.now().date()
            next_week = today + timedelta(days=7)
            
            # Total upcoming
            cur.execute("""
                SELECT COUNT(*) FROM appointments 
                WHERE user_id = %s AND status = 'Upcoming' AND DATE(date_time) >= %s
            """, (current_user.id, today))
            upcoming_count = cur.fetchone()['COUNT(*)']
            
            # Upcoming in next 7 days
            cur.execute("""
                SELECT COUNT(*) FROM appointments 
                WHERE user_id = %s AND status = 'Upcoming' AND DATE(date_time) BETWEEN %s AND %s
            """, (current_user.id, today, next_week))
            upcoming_week_count = cur.fetchone()['COUNT(*)']
            
            # Completed
            cur.execute("""
                SELECT COUNT(*) FROM appointments 
                WHERE user_id = %s AND status = 'Completed'
            """, (current_user.id,))
            completed_count = cur.fetchone()['COUNT(*)']
            
            # Cancelled
            cur.execute("""
                SELECT COUNT(*) FROM appointments 
                WHERE user_id = %s AND status = 'Cancelled'
            """, (current_user.id,))
            cancelled_count = cur.fetchone()['COUNT(*)']
            
            return render_template('appointments.html', 
                               appointments=appointments,
                               status_filter=status_filter,
                               date_filter=date_filter,
                               sort_by=sort_by,
                               upcoming_count=upcoming_count,
                               upcoming_week_count=upcoming_week_count,
                               completed_count=completed_count,
                               cancelled_count=cancelled_count)
    finally:
        conn.close()

@app.route('/appointments/add', methods=['GET', 'POST'])
@login_required
def add_appointment():
    if request.method == 'POST':
        provider_name = request.form['provider_name']
        date_time = request.form['date_time']
        reason = request.form['reason']
        status = request.form['status']
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO appointments 
                    (user_id, provider_name, date_time, reason, status) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (current_user.id, provider_name, date_time, reason, status))
                conn.commit()
                flash('Appointment added successfully', 'success')
                return redirect(url_for('appointments'))
        finally:
            conn.close()
    
    return render_template('add_edit_appointment.html', appointment=None)

@app.route('/appointments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_appointment(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM appointments WHERE id = %s AND user_id = %s", (id, current_user.id))
            appointment = cur.fetchone()
            
            if not appointment:
                flash('Appointment not found or access denied', 'danger')
                return redirect(url_for('appointments'))
            
            # Convert datetime to string for the template if it exists
            if appointment and 'date_time' in appointment and appointment['date_time']:
                appointment['date_time_str'] = appointment['date_time'].strftime('%Y-%m-%dT%H:%M')
            
            if request.method == 'POST':
                provider_name = request.form['provider_name']
                date_time = request.form['date_time']
                reason = request.form['reason']
                status = request.form['status']
                
                cur.execute("""
                    UPDATE appointments 
                    SET provider_name = %s, date_time = %s, reason = %s, status = %s 
                    WHERE id = %s AND user_id = %s
                """, (provider_name, date_time, reason, status, id, current_user.id))
                conn.commit()
                flash('Appointment updated successfully', 'success')
                return redirect(url_for('appointments'))
            
            return render_template('add_edit_appointment.html', appointment=appointment)
    finally:
        conn.close()

@app.route('/appointments/delete/<int:id>', methods=['POST'])
@login_required
def delete_appointment(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM appointments WHERE id = %s AND user_id = %s", (id, current_user.id))
            conn.commit()
            affected_rows = cur.rowcount
            
            if affected_rows > 0:
                flash('Appointment deleted successfully', 'success')
            else:
                flash('Appointment not found or access denied', 'danger')
            
            return redirect(url_for('appointments'))
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)