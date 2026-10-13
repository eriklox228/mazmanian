from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User, Request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'k'
db.init_app(app)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        f = request.form
        if User.query.filter_by(login=f['login']).first():
            return render_template('register.html', error='Логин занят')
        u = User(login=f['login'], password=f['password'], fullname=f['fullname'],
                 phone=f['phone'], email=f['email'])
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = User.query.filter_by(login=request.form['login'],
                                 password=request.form['password']).first()
        if u:
            session['user_id'] = u.id
            session['is_admin'] = u.is_admin
            return redirect(url_for('my_requests'))
        return render_template('login.html', error='Неверный логин или пароль')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/create_request', methods=['GET', 'POST'])
def create_request():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        r = Request(user_id=session['user_id'], room=request.form['room'],
                    start_date=request.form['start_date'],
                    payment=request.form['payment'], status='Новая')
        db.session.add(r)
        db.session.commit()
        return redirect(url_for('my_requests'))
    return render_template('create_request.html')

@app.route('/my_requests')
def my_requests():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    reqs = Request.query.filter_by(user_id=session['user_id']).all()
    return render_template('my_requests.html', requests=reqs)

@app.route('/add_review/<int:rid>', methods=['POST'])
def add_review(rid):
    r = Request.query.get(rid)
    r.review = request.form['review']
    db.session.commit()
    return redirect(url_for('my_requests'))

@app.route('/admin')
def admin():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    return render_template('admin.html', requests=Request.query.all())

@app.route('/update_status/<int:rid>', methods=['POST'])
def update_status(rid):
    r = Request.query.get(rid)
    r.status = request.form['status']
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(login='Conf2027').first():
            a = User(login='Conf2027', password='Demo77', fullname='Админ',
                     phone='8(999)999-99-99', email='a@a.ru', is_admin=True)
            db.session.add(a)
            db.session.commit()
    app.run(debug=True, port=8080)