from django.forms import formsets
from django.forms.forms import Form
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from .models import FollowUser, MyPost, MyProfile, PostLike
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.http.response import HttpResponseRedirect
from datetime import datetime


from .models import PostComment
from .forms import CommentForm
from . import views

def registerPage(request):
    context = {}
    return render(request, 'accounts/register.html',context)


# Create your views here.
@method_decorator(login_required, name="dispatch")    
class HomeView(TemplateView):

    template_name = "cat/home.html"
    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)

        # si = self.request.GET.get("si")
        # if si == None:
        #     si = ""
        # posts = MyPost.objects.filter(Q(uploaded_by__in = self.request.user.myprofile)).filter(Q(subject_icontains = si)) | (Q(subject_icontains = si)).order_by("-id")
        # context["mypost_list"] = posts
        # return context
        # postList = MyPost.objects.filter(uploaded_by__in = self.request.user).order_by("-id")
        
        
        
        followedList = FollowUser.objects.filter(followed_by = self.request.user.myprofile)
        followedList2 = []
        for e in followedList:
            followedList2.append(e.profile)
        postList = MyPost.objects.filter(uploaded_by__in = followedList2).order_by("-id")
        
        for p1 in postList:
            p1.liked = False
            ob = PostLike.objects.filter(post = p1,liked_by=self.request.user.myprofile)
            if ob:
                p1.liked = True        
            obList = PostLike.objects.filter(post = p1)
            p1.likedno = obList.count()
        context["mypost_list"] = postList
        return context

  
class AboutView(TemplateView):
    template_name = "cat/about.html"

class ContactView(TemplateView):
    template_name = "cat/contact.html"


def follow(req, pk):
    user = MyProfile.objects.get(pk=pk)
    FollowUser.objects.create(profile=user, followed_by = req.user.myprofile)
    return HttpResponseRedirect(redirect_to="/cat/myprofile")

def unfollow(req, pk):
    user = MyProfile.objects.get(pk=pk)
    FollowUser.objects.filter(profile=user, followed_by = req.user.myprofile).delete()
    return HttpResponseRedirect(redirect_to="/cat/myprofile")

def like(req, pk):
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.create(post=post, liked_by = req.user.myprofile)
    return HttpResponseRedirect(redirect_to="/cat/home")

def unlike(req, pk):
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.filter(post=post, liked_by = req.user.myprofile).delete()
    return HttpResponseRedirect(redirect_to="/cat/home")


@method_decorator(login_required, name="dispatch")    
class MyProfileUpdateView(UpdateView):
    model = MyProfile
    fields = ["name", "age","address", "status", "gender", "phone_no", "description", "pic"]

@method_decorator(login_required, name="dispatch")    
class MyPostCreate(CreateView):
    model = MyPost
    fields = ["subject", "msg", "pic"]
    def form_valid(self, form):
        self.object = form.save()
        self.object.uploaded_by = self.request.user.myprofile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())




@method_decorator(login_required, name="dispatch")    
class MyPostListView(ListView):
    model = MyPost
    def get_queryset(self):
        si = self.request.GET.get("si")
        if si == None:
            si = ""
        return MyPost.objects.filter(Q(uploaded_by = self.request.user.myprofile)).filter(Q(subject__icontains = si) | Q(msg__icontains = si)).order_by("-id")
 
@method_decorator(login_required, name="dispatch")    
class MyPostDetailView(DetailView):
    model = MyPost
    

@method_decorator(login_required, name="dispatch")  
def MyPostDetail(request,pk):
    mypost = MyPost.objects.get(id=pk)

    num_comments = PostComment.objects.filter(product=mypost).count()

    context = {
        'mypost' : mypost,
        'num_comments' : num_comments
        }


@method_decorator(login_required, name="dispatch")    
class MyPostDeleteView(DeleteView):
    model = MyPost

@method_decorator(login_required, name="dispatch")    
class MyProfileListView(ListView):
    model = MyProfile
    def get_queryset(self,):
        si = self.request.GET.get("si")
        if si == None:
            mypost_list = MyProfile.objects.all()
            # context = {'mypost_list' : mypost_list}
            for p1 in mypost_list:
                p1.followed = False
                ob = FollowUser.objects.filter(profile = p1,followed_by=self.request.user.myprofile)
                if ob:
                    p1.followed = True
            return mypost_list
        else:
            profList = MyProfile.objects.filter(Q(name__icontains = si) | Q(address__icontains = si) | Q(gender__icontains = si) | Q(status__icontains = si)).order_by("-id")
            for p1 in profList:
                p1.followed = False
                ob = FollowUser.objects.filter(profile = p1,followed_by=self.request.user.myprofile)
                if ob:
                    p1.followed = True
            return profList

@method_decorator(login_required, name="dispatch")    
class MyProfileDetailView(DetailView):
    model = MyProfile





@login_required
def add_comment(request, pk):
    mypost = MyPost.objects.get(id=pk)
    form = CommentForm(instance=MyPost)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance= mypost)
        if form.is_valid():
            
            name = request.user
            body = form.cleaned_data['msg']

            # self.object.uploaded_by = self.request.user.myprofile
            c = PostComment(post= mypost, commented_by=name, msg=body, cr_date=datetime.now())

            c.save()
            return redirect(f'/cat/mypost/{pk}')
        else:
            print('form is invalid')    
    else:
        form = CommentForm()    


    context = {
        'form': form
    }

    return render(request, 'cat/add_comment.html', context)



@method_decorator(login_required, name="dispatch")    
class PostCommentDeleteView(DeleteView):
    model = PostComment