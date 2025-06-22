from flask import Flask, render_template, url_for, request, abort, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///residents.db"
db = SQLAlchemy (app)


class Resident(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] =  mapped_column(nullable=False)
    room:Mapped[int] =  mapped_column(default=000)
    telephone_number =  db.Column(db.String(15), default = '+79521234567')
    
    def __repr__(self):
        return '<Resident %r>' % self.id

    

ALLOWED_IPS = [
        '127.0.0.1'
]

@app.before_request
def check_ip():
    client_ip = request.remote_addr
    if client_ip not in ALLOWED_IPS:
        abort(403, description="Ваш IP не разрешен")


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return (f'{name} page , \n id:{id}')


@app.route('/residents')
def residents():
    residents = Resident.query.order_by(Resident.room).all()
    return render_template('residents.html', residents=residents)



@app.route('/residents/<int:id>')
def resident_profile(id):
    resident = Resident.query.get(id)
    return render_template('resident_profile.html', resident=resident)




@app.route('/create-resident', methods=['POST', 'GET'])
def create_resident():
    if request.method == 'POST':
        name = request.form["name"]
        room = request.form["room"]
        telephone_number = request.form["telephone_number"]

        resident=Resident(name=name, room=room, telephone_number=telephone_number)

        try:
            db.session.add(resident)
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибка при записи"
    else:
        return (render_template('create_resident.html'))




if __name__ == "__main__":
    app.run(debug=True)
    