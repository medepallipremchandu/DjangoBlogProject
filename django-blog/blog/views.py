from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = f"Message from {name}"
            body = f"Sender's email: {email}\n\nMessage:\n{message}"
            
            # Create and send the email
            email_message = EmailMessage(
                subject=subject,
                body=body,
                from_email=email,  # Sender's email address from the form
                to=['2000031715cse@gmail.com'],  # Replace with your recipient's email address
                reply_to=[email],  # Set the reply-to address to sender's email
            )
            email_message.send()
            
            return render(request, 'blog/success.html')  # Display a success page
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})

from .models import Post, Comment, Category
from .forms import CommentForm

def blog_index(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(title__icontains=query).order_by("-created_on")
    else:
        posts = Post.objects.all().order_by("-created_on")

    paginator = Paginator(posts, 5)  # 5 posts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    categories = Category.objects.all()
    
    return render(request, 'blog/index.html', {'posts': posts, 'query': query, 'categories': categories})

def blog_category(request, category):
    posts = Post.objects.filter(categories__name__contains=category).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)

def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }

    return render(request, "blog/detail.html", context)

