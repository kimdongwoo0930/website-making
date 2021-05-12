
from django.contrib.admin.filters import RelatedFieldListFilter
from django.core import paginator
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from .models import Board
from .forms import Boardform
from user.models import user
from django.http import Http404
from tag.models import Tag

# Create your views here.
def board_detail(request,pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404("게시글을 찾을수 없습니다.")
    return render(request,'board_detail.html',{'board' : board})

def board_write(request):
    if not request.session.get("user"):
        return redirect('/user/login/')
    
    if request.method == "POST":
        form = Boardform(request.POST)
        if form.is_valid():
            user_id = request.session.get('user')
            User =  user.objects.get(pk=user_id)

            tags = form.cleaned_data['tags'].split(',')
            board = Board()
            board.title = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']
            board.writer = User
            board.save()
            for tag in tags:
                if not tag:
                    continue

                _tag,  _  = Tag.objects.get_or_create(name=tag)
                board.tags.add(_tag)

            return redirect('/board/list/')

    else:

        form = Boardform()
    return render(request, 'board_write.html',{'form':form})




def board_list(request):
    all_boards = Board.objects.all().order_by("-id")
    page = int(request.GET.get('p',1))
    paginator = Paginator(all_boards,5) 

    boards = paginator.get_page(page)

    return render(request, 'boardlist.html',{'boards': boards})