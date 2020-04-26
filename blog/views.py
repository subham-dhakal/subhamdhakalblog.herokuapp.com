from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
# from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector



# FBV of post_list
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug= tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # 3 post on each page
    page = request.GET.get('page')      # get current page
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  # deliver last page of results

    return render(request, 'blog/post/list.html', {'posts':posts, 'page':page, 'tag':tag})


# CBV of post_list
# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'
#




def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                                            publish__year =year, 
                                            publish__month=month, 
                                             publish__day=day)

    # list  of active comments for this post
    comments = post.comments.filter(active=True)  # ( current_obj . Foreign key vako class ko related_name . fields)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # Create comment object but dont save to the database
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # save comment to the database
            new_comment.save()
            # return redirect('blog:post_detail')

    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html',{'post':post, 'comment_form':comment_form, 'comments':comments, 'new_comment':new_comment})



def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="published")
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({})  recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'subhamdhakal123@gmail.com',[cd['to']], fail_silently=False)
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',{'post':post,'form':form,'sent':sent})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(search = SearchVector('title', 'body')).filter(search=query)

    return render(request, 'blog/post/search.html', {'form':form, 'query':query, 'results':results})
