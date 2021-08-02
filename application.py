from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"

@app.route('/')
def index():
    return 'Sup Bitch!'

@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()

    output = []
    for drink in drinks:
        drink_data = {'name': drink.name, 'description': drink.description}
        output.append(drink_data)

    return {"drinks": output}

@app.route('/drinks/<id>')
# id starts at 1, e.g., http://127.0.0.1/drinks/4
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {"name": drink.name, "description": drink.description}


@app.route('/drinks', methods=['POST'])
def add_drink():
    drink = Drink(
                name=request.json['name'],
                description=request.json['description']
            )
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id}

@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return{"error": "not found"}
    db.session.delete(drink)
    db.session.commit()
    return {
            "message": "%s described as %s was just y33ted tf out!" 
            %(drink.name, drink.description)
        }

# testing PUT request
@app.route('/drinks', methods=['PUT'])
def replace_drink():
    drink = Drink.query.filter_by(name = request.json['name']).first()
    if drink is None:
        return {"error": "%s not found" %request.json['name']}
    delete_drink(drink.id)
    add_drink()
    return {'id': drink.id}