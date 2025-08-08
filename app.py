from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import bcrypt
import os
import certifi
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'fabtech_secret'

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI, tls=True, tlsCAFile=certifi.where())  # ✅ FIXED LINE
db = client["fabtech_store"]
users_collection = db["users"]


# ------------------------ Routes ------------------------

# ----------- Landing Page (Welcome) -----------
@app.route('/')
def index():
    return render_template('index.html')

# ----------- Registration -----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        if users_collection.find_one({"username": username}):
            return "Username already exists. Please try another."

        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
        users_collection.insert_one({"username": username, "password": hashed_pw})
        return redirect(url_for('login'))
    return render_template('register.html')

# ----------- Login -----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        user = users_collection.find_one({"username": username})

        if user and bcrypt.checkpw(password, user['password']):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return "Invalid credentials. Try again."
    return render_template('login.html')

# ----------- Logout -----------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ----------- Dashboard -----------
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# ----------- Add to Cart (Single Product) -----------
@app.route('/cart')
def cart():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('cart.html')



@app.route('/successcart')
def successcart():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('successcart.html')



# ----------- Buy Now (Single Product Purchase) -----------
@app.route('/buy-now', methods=['POST'])
def buy_now():
    if 'username' not in session:
        return redirect(url_for('login'))

    product_name = request.form['name']
    product_price = request.form['price']
    product_image = request.form['image']

    session['buy_now_product'] = {
        'name': product_name,
        'price': product_price,
        'image': product_image
    }
    return redirect(url_for('success'))

# ----------- Purchase Success Page -----------
@app.route('/success')
def success():
    if 'username' not in session:
        return redirect(url_for('login'))

    product = session.get('buy_now_product')
    return render_template('success.html', product=product)


# Route for individual product page
@app.route('/product', methods=['GET'])
def product():
    name = request.args.get('name')
    price = request.args.get('price')
    image = request.args.get('image')
    return render_template('product.html', name=name, price=price, image=image)






# -------------------- Run App --------------------
if __name__ == '__main__':
    app.run(debug=True)
