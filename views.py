from flask import render_template, request, redirect, flash
from models import Category, MayaClothes, Age, db
from mayaclothesapp import app


@app.route('/')
def list_all():
    return render_template(
        'list.html',
        categories=Category.query.all(),
        mayaclothes=MayaClothes.query.join(Age).order_by(Age.value.desc())
    )


@app.route('/<name>')
def list_mayaclothes(name):
    category = Category.query.filter_by(name=name).first()
    return render_template(
        'list.html',
        mayaclothes=MayaClothes.query.filter_by(category=category).join(Age).order_by(Age.value.desc()),
        categories=Category.query.all(),
    )

@app.route('/new-item', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        category = Category.query.filter_by(id=request.form['category']).first()
        age = Age.query.filter_by(id=request.form['age']).first()
        mayaclothes = MayaClothes(category=category, age=age, description=request.form['description'])
        db.session.add(mayaclothes)
        db.session.commit()
        return redirect('/')
    else:
        return render_template(
            'new-item.html',
            page='new-item',
            categories=Category.query.all(),
            ages=Age.query.all()
        )


@app.route('/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    mayaclothes = MayaClothes.query.get(item_id)
    if request.method == 'GET':
        return render_template(
            'new-item.html',
            mayaclothes=mayaclothes,
            categories=Category.query.all(),
            ages=Age.query.all()
        )
    else:
        category = Category.query.filter_by(id=request.form['category']).first()
        age = Age.query.filter_by(id=request.form['age']).first()
        description = request.form['description']
        mayaclothes.category = category
        mayaclothes.age = age
        mayaclothes.description = description
        db.session.commit()
        return redirect('/')


@app.route('/new-category', methods=['GET', 'POST'])
def new_category():
    if request.method == 'POST':
        category = Category(name=request.form['category'])
        db.session.add(category)
        db.session.commit()
        return redirect('/')
    else:
        return render_template(
            'new-category.html',
            page='new-category.html')

@app.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    category = Category.query.get(category_id)
    if request.method == 'GET':
        return render_template(
            'new-category.html',
            category=category
        )
    else:
        category_name = request.form['category']
        category.name = category_name
        db.session.commit()
        return redirect('/')

@app.route('/delete-category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    if request.method == 'POST':
        category = Category.query.get(category_id)
	items = MayaClothes.query.filter_by(category=category).first()
        if not items:
            db.session.delete(category)
            db.session.commit()
        else:
            flash('You have Items in that category. Remove them first.')
        return redirect('/')

@app.route('/delete-item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    if request.method == 'POST':
        item = MayaClothes.query.get(item_id)
        db.session.delete(item)
        db.session.commit()
        return redirect('/')

