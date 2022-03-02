from webapp import app, db
from webapp.forms import LoginForm, RegistrationForm, Fitur1Form, FiturTambahSiswa
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from webapp.models import User, Siswa
from werkzeug.urls import url_parse
from collections import Counter

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('invalid username or password')
			return redirect(url_for('login'))
		
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('main')
		return redirect(next_page)

	return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/')
@login_required
def main():
	return render_template('home.html')

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main'))

@app.route('/fitur1', methods=['GET', 'POST'])
@login_required
def fitur1():
	titel = "FITUR 1"
	form = Fitur1Form()
	if form.validate_on_submit():
		angka = int(form.angka.data)
		x = angka % 2
		if angka < 10:
			if x == 0:
				color = "red"
			else:
				color = "blue"
		else:
			if x == 0:
				color = "green"
			else:
				color = "yellow"
		return render_template('fitur1_aksi.html', angka=angka+1, color=color)
	return render_template('fitur1.html', form=form, titel=titel)

@app.route('/fitur1/aksi', methods=['GET','POST'])
@login_required
def fitur1_aksi():
	return render_template('fitur1_aksi.html')

@app.route('/fitur2', methods=['GET','POST'])
@login_required
def fitur2():
	form = FiturTambahSiswa()
	siswa = Siswa.query.all()
	return render_template('fitur2.html', siswa=siswa, form=form)

@app.route('/fitur2/tambahsiswa', methods=['GET','POST'])
@login_required
def tambah_siswa():
	form = FiturTambahSiswa()
	siswa = Siswa.query.all()
	if form.validate_on_submit():
		nama = form.nama.data
		jkel = form.jkel.data
		siswa = Siswa(nama_siswa=nama, jkel=jkel)
		db.session.add(siswa)
		db.session.commit()
		return redirect(url_for('fitur2'))
	return render_template('fitur2.html', siswa=siswa, form=form)

@app.route('/fitur2/edit_siswa?<id_siswa>', methods=['GET','POST'])
@login_required
def edit_siswa(id_siswa):
	form = FiturTambahSiswa()
	siswa = Siswa.query.filter_by(id=id_siswa).first()
	if siswa.jkel == 'L':
		l = "checked"
		p = " "
	else:
		l = " "
		p = "checked"
	return render_template('editsiswa.html', nama_siswa=siswa.nama_siswa, l=l,p=p, form=form, id=id_siswa)

@app.route('/fitur2/edit_siswa?<id_siswa>/simpan', methods=['GET','POST'])
@login_required
def simpan_edit_siswa(id_siswa):
	nama = request.form['nama']
	jkel = request.form['jkel']
	siswa = Siswa.query.filter(Siswa.id == id_siswa).one()
	siswa.nama_siswa = nama
	siswa.jkel = jkel
	db.session.commit()
	return redirect(url_for('fitur2'))

@app.route('/fitur2/hapus_siswa?<id_siswa>', methods=['GET','POST'])
@login_required
def hapus_siswa(id_siswa):
	id = id_siswa
	siswa = Siswa.query.filter(Siswa.id == id_siswa).delete()
	db.session.commit()
	return redirect(url_for('fitur2'))

@app.route('/fitur3')
@login_required
def fitur3():
	form = FiturTambahSiswa()
	return render_template('fitur3.html',form=form)

@app.route('/fitur3/hasil', methods=['GET','POST'])
@login_required
def fitur3_aksi():
	a = request.form['a'].lower()
	b = request.form['b'].lower()
	count_a = Counter(a)
	count_b = Counter(b)
	size_a = len(count_a)
	temp = 0
	sama = []

	for char_a, c_a in count_a.most_common():
		for char_b, c_b in count_b.most_common():
			if char_a == char_b:
				temp += 1
				sama.append(char_a)

	jml = temp
	persen = (jml / size_a)* 100;

	return render_template('fitur3_aksi.html',a=a,b=b,size_a=size_a,count_a=count_a,sama=sama,persen=persen)