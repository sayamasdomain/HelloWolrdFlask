from flask import Flask, render_template, request, redirect, url_for
from peewee import *

db = 'barang.db'

database = SqliteDatabase(db)

class BaseModel(Model):
	class Meta:
		database=database

class Barang(BaseModel):
	id = AutoField(primary_key=True)
	nama_barang = CharField()
	harga_barang = IntegerField()

def create_tables():
	with database:
		database.create_tables([Barang])

app = Flask(__name__)


@app.route('/')
def index():
	barang = Barang.select()
	return render_template('card.html', barang=barang)

@app.route('/insert_barang',methods=['GET','POST'])
def insert_barang():
	if request.method == 'GET':
		return render_template('insert_barang.html')
	else:
		nama_barang = request.form['nama_barang']
		harga_barang = request.form['harga_barang']

		# insert to database
		Barang.create(nama_barang=nama_barang,harga_barang=harga_barang)
		return redirect(url_for('index'))

@app.route('/delete_barang/<id_barang>')
def delete_barang(id_barang):
	del_barang = Barang.delete().where(Barang.id == id_barang)
	del_barang.execute()
	return redirect(url_for('index'))

@app.route('/update_barang/<id_barang>',methods=['GET','POST'])
def update_barang(id_barang):
	if request.method == 'GET':
		barang = Barang.select().where(Barang.id == id_barang)
		barang = barang.get()
		return render_template('update_barang.html',barang=barang)
	else:
		nama_barang = request.form['nama_barang']
		harga_barang = request.form['harga_barang']

		upd_barang = Barang.update(nama_barang=nama_barang,harga_barang=harga_barang).where(Barang.id == id_barang)
		upd_barang.execute()
		return redirect(url_for('index'))


if __name__ == '__main__':
	create_tables()
	app.run(debug=True)