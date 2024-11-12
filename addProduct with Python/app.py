from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'  # Leave empty if no password set
app.config['MYSQL_DB'] = 'ecommerce'

mysql = MySQL(app)

# Initialize MySQL
mysql = MySQL(app)

# Root route
@app.route('/')
def home():
    return redirect(url_for('add_product'))

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['productName']
        price = request.form['productPrice']
        description = request.form['productDescription']
        category = request.form['productCategory']
        
        # Handle file upload
        if 'productImage' in request.files:
            image = request.files['productImage']
            if image.filename != '':
                image_path = os.path.join('uploads', image.filename)
                full_path = os.path.join('static', image_path)
                image.save(full_path)
            else:
                image_path = None
        
        # Insert into database
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO products (name, price, description, category, image_path)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, price, description, category, image_path))
        mysql.connection.commit()
        cur.close()
        
        # Redirect to dashboard
        return redirect(url_for('seller_dashboard'))
    
    return render_template('add_product.html')

@app.route('/seller_dashboard')
def seller_dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products ORDER BY id DESC")
    products = cur.fetchall()
    cur.close()
    return render_template('seller_dashboard.html', products=products)

if __name__ == '__main__':
    # Create uploads folder if it doesn't exist
    os.makedirs(os.path.join('static', 'uploads'), exist_ok=True)
    app.run(debug=True)