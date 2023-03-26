
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.contrib.auth.decorators import login_required
from board.models import Care, Comment, ReComment
from .forms import CareForm, CommentForm
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages


def home(request):
    posts = Care.objects.order_by('-created_at')

    # 정렬 기준
    sort = request.GET.get('sort', "created_at")
    # 검색어 받기
    keyword = request.GET.get("keyword", "")
    # 검색기준 : 댓글순, 추천수, 최신순
    search_kinds = request.POST.get('search_kinds', "")

    if sort == 'view_count':
        posts = Care.objects.order_by('-view_count', '-created_at')
    elif sort == 'comment_count':
        posts = Care.objects.order_by('-comment_count', '-created_at')
        # posts = Care.objects.annotate(com_cut=Count(
        #     'comment')).order_by('comment_count', '-created_at')
    elif sort == 'best':
        posts = Care.objects.annotate(best_cnt=Count(
            'best')).order_by('-best_cnt', '-created_at')
    else:
        posts = Care.objects.order_by('-created_at')

    # 검색어가 들어간 리스트만 추출
    if keyword:
        if search_kinds == 'all':
            posts = posts.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword) | Q(
                place__icontains=keyword) | Q(writer__name__icontains=keyword)).distinct()

        elif search_kinds == "title":
            posts = posts.filter(title__icontains=keyword).distinct()

        elif search_kinds == "writer":
            posts = posts.filter(writer__name__icontains=keyword).distinct()

        elif search_kinds == "content":
            posts = posts.filter(content__icontains=keyword).distinct()
        else:
            posts = posts.filter(place__icontains=keyword).distinct()

    # 현재 페이지 번호
    page = request.GET.get("page", 1)

    paginator = Paginator(posts, 4)
    list = paginator.get_page(page)

    return render(request, 'board/board_index.html', {'list': list, 'sort': sort, 'page': page, 'keyword': keyword})


# 글작성


@login_required(login_url="login")
def update(request):
    if request.method == "POST":
        form = CareForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post. writer = request.user
            post.save()
            form.save_m2m()
            return redirect("board_index")
    else:
        form = CareForm()
    return render(request, "board/board_write.html", {"form": form})

# 글 디테일


def detail(request, pk):
    post = get_object_or_404(Care, pk=pk)
    default_view_count = post.view_count
    post.view_count = default_view_count + 1
    post.save()
    return render(request, "board/board_detail.html", {"post": post})


#  글 삭제
@login_required(login_url="login")
def remove(request, pk):
    post = get_object_or_404(Care, pk=pk)
    post.delete()
    return redirect("board_index")

# 글 수정


@login_required(login_url="login")
def edit(request, pk):
    post = Care.objects.get(pk=pk)
    if request.method == "POST":
        form = CareForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = request.user
            post.save()
            form.save_m2m()
            return redirect("board_index")
    else:
        form = CareForm(instance=post)
    return render(request, "board/board_edit.html", {"form": form})


# 댓글작성
@login_required(login_url="login")
def comment_create(request, post_pk):
    """
    댓글내용, 원본글 번호, 작성자(로그인 사용자)
    """
    post = get_object_or_404(Care, pk=post_pk)
    post.comment_count = post.comment_count + 1
    post.save()

    if request.method == "POST":
        comment = Comment()
        comment.post = post
        comment.writer = request.user
        comment.contents = request.POST['contents']
        comment.save()

    return redirect("board_detail", pk=post_pk)
# 댓글삭제


@login_required(login_url="login")
def comment_remove(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect('board_detail', post_pk)


# 댓글 수정
@login_required(login_url="login")
def comment_update(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.writer = request.user
            # comment.contents = request.POST['contents']
            comment.save()
            return redirect("board_detail", post_pk)
    else:
        form = CareForm(instance=comment)
    return render(request, "board/comment_update.html", {"form": form})


# 대댓글
@login_required(login_url="login")
def comment_write(request, post_pk, comment_pk):
    """
    댓글내용, 원본글 번호, 작성자(로그인 사용자)
    """

    answer = get_object_or_404(Comment, pk=comment_pk)
    if request.method == "POST":
        recomment = ReComment()
        recomment.answer = answer
        recomment.writer = request.user
        recomment.contents = request.POST['contents']
        recomment.save()

        return redirect(request, "board_detail", comment_pk, post_pk)


@login_required(login_url="login")
def vote_question(request, post_id):

    post = get_object_or_404(Care, id=post_id)

    if post.writer != request.user:
        post.best.add(request.user)
    else:
        messages.error(request, "본인이 작성한 글은 추천할 수 없습니다.")

    return redirect("board_detail", pk=post_id)
