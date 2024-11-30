from collections import UserDict
from app import app,login_manager,db,photos,search
from flask import render_template,session,flash,redirect,url_for,request,current_app
from flask_login import login_required,current_user,logout_user,login_user
from flask_ckeditor import CKEditor
from datetime import datetime
from .forms import BlogPost
from .models import Category,Post
from ..models import User
from ..forms import RegisterUser
import os
import secrets

@app.route('/')
def home():
    page=request.args.get('page',1,type=int)
    post=Post.query.order_by(Post.id.desc()).paginate(page=page,per_page=4)
    categories=Category.query.join(Post,(Category.id==Post.category_id)).all()
    return render_template('/dashboard/home.html',post=post,categories=categories)

@app.route('/result')
def result():
    categories=Category.query.join(Post,(Category.id==Post.category_id)).all()
    searchword=request.args.get('q')
    post=Post.query.msearch(searchword,fields=['title','content'],limit=6)
    return render_template('/dashboard/result.html',post=post,categories=categories)

@app.route('/single_blog/<int:id>')
def single_blog(id):
    categories=Category.query.join(Post,(Category.id==Post.category_id)).all()
    post=Post.query.get_or_404(id)
    return render_template('/dashboard/single_blog.html',post=post,categories=categories)


@app.route('/dashboard')
@login_required
def dashboard():
    posts=Post.query.all()
    user=User.query.all()
    return render_template('/dashboard/dashboard.html',username=session['username'],posts=posts,user=user)


@app.route('/profile')
@login_required
def profile():
    id = current_user.id 
    user = User.query.get_or_404(id)
    return render_template('/dashboard/profile.html', user=user)

@app.route('/edit/profile/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_profile(id):
    user = User.query.get_or_404(id)
    form = RegisterUser()

    if request.method == 'POST':
        user.name = form.name.data
        user.username = form.username.data

        if request.files.get('profile'):
            try:
                # Deleting the old profile picture if exists
                if user.profile:  # Check if the user has a profile picture
                    os.unlink(os.path.join(current_app.root_path, 'static/pictures/' + user.profile))
                
                # Save the new profile picture
                user.profile = photos.save(request.files.get('profile'), name=secrets.token_hex(10) + '.')
            except:
                # Save the new profile picture if deletion fails
                user.profile = photos.save(request.files.get('profile'), name=secrets.token_hex(10) + '.') 

        db.session.commit()
        flash('Account Updated Successfully', 'success')

    elif request.method == 'GET':
        form.name.data = user.name
        form.username.data = user.username

    return render_template('/dashboard/edit_profile.html', form=form, user=user)



@app.route('/blog/post',methods=['POST','GET'])
@login_required
def blog_post():
    categories=Category.query.all()
    form=BlogPost()
    if  form.validate_on_submit() and request.method=='POST':
        title=form.title.data
        content=form.content.data
        category=request.form.get('category')
        pic=photos.save(request.files.get('image'),name=secrets.token_hex(10) + '.')
        author=current_user.id
        date_posted=datetime.now()
        post=Post(title=title,content=content,category_id=category,image=pic,author_id=author,date_posted=date_posted)
        db.session.add(post)
        db.session.commit()
        flash('Blog Post Added Successfully','success')
    return render_template('/dashboard/blog_post.html',form=form,categories=categories)


@app.route('/edit_post/<int:id>',methods=['GET','POST'])
@login_required
def edit_posts(id):
    categories=Category.query.all()
    post=Post.query.get_or_404(id)
    category=request.form.get('category')
    form=BlogPost()
    if  form.validate_on_submit() and request.method=='POST':
        post.title=form.title.data
        post.content=form.content.data
        post.category_id=category
        if request.files.get('image'):
            try:
                os.unlink(os.path.join(current_app.root_path,'static/pictures/' + post.image))
                post.image = photos.save(request.files.get('image'),name=secrets.token_hex(10) + '.')
            except:
                post.image = photos.save(request.files.get('image'),name=secrets.token_hex(10) + '.')
        db.session.commit()
    elif request.method=='GET':
        form.title.data=post.title
        form.content.data=post.content
    return render_template('/dashboard/edit_post.html',form=form,post=post,categories=categories)


@app.route('/delete_post/<int:id>',methods=['POST','GET'])
def delete_post(id):
    post=Post.query.get_or_404(id)
    if request.method=='POST':
        if request.files.get('image'):
            try:
                os.unlink(os.path.join(current_app.root_path,'static/pictures/' + post.image))
            except Exception as e:
                print(e)
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('dashboard'))


#get category
@app.route('/category/<int:id>')
def get_category(id):
    page=request.args.get('page',1,type=int)
    get_cat=Category.query.filter_by(id=id).first_or_404()
    categories=Category.query.join(Post,(Category.id==Post.category_id)).all()
    category=Post.query.filter_by(category=get_cat).paginate(page=page,per_page=4)
    return render_template('/dashboard/home.html',category=category,categories=categories,get_cat=get_cat)

@app.route('/blog/category',methods=['POST','GET'])
@login_required
def blog_category():
    if request.method=='POST':
        category=request.form.get('category')
        categories=Category(name=category)
        db.session.add(categories)
        flash('Category added successfully','success')
        db.session.commit()
    return render_template('/dashboard/category.html')