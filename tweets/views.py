#from django.core.serializers import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.template.loader import render_to_string
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from user_profile.models import User, UserFollowers
from user_profile.forms import RegisterForm
from tweets.models import Tweet, HashTag
from tweets.forms import TweetForm, SearchForm
import json


TWEET_PER_PAGE = 5


# Create your views here.

class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class Index(View):
    def get(self, request):
        params = {"name": "Django", "version": "1.8"}
        return render(request, 'base.html', params)

    def post(self):
        return HttpResponse('post request')


class Profile(LoginRequiredMixin, View):
    """	User profile page reachable from /user/<username> URL	"""

    def get(self, request, username):
        params = {}
        userProfile = User.objects.get(username=username)
        #userFollower = UserFollowers.objects.get(user=userProfile)
        try:
            userFollower = UserFollowers.objects.get(user=userProfile)
            if userFollower.followers.filter(username=request.user.username).exists():
                params["following"] = True
            else:
                params["following"] = False
        except:
            userFollower = []
        form = TweetForm(initial={'country': 'Global'})
        search_form = SearchForm()
        tweets = Tweet.objects.filter(user=userProfile).order_by('-created_date')
        paginator = Paginator(tweets, TWEET_PER_PAGE)
        page = request.GET.get('page')
        try:
            tweets = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            tweets = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            tweets = paginator.page(paginator.num_pages)
        params["tweets"] = tweets
        params["profile"] = userProfile
        params["form"] = form
        params["search"] = search_form
        return render(request, 'profile.html', params)

    def post(self, request, username):
        follow = request.POST['follow']
        user = User.objects.get(username= request.user.username)
        userProfile = User.objects.get(username=username)
        userFollower, status = UserFollowers.objects.get_or_create(user=userProfile)
        userFollower.count += 1
        userFollower.save()
        if follow == 'true':
            #follow user
            userFollower.followers.add(user)
        else:
            #unfollow user
            userFollower.followers.remove(user)
        return HttpResponse(json.dumps(""), content_type="application/json")


class PostTweet(View):
    """	Tweet post form available on page /user/<username> URL	"""

    def post(self, request, username):
        # form = TweetForm(self.request.POST)
        user = User.objects.get(username=username)
        tweet = Tweet(text=request.POST.get('text'),
                      user=user,
                      country='UA')
        tweet.save()
        words = request.POST.get('text').split(" ")
        for word in words:
            if word[0] == '#':
                hasht, created = HashTag.objects.get_or_create(name=word[1:])
                hasht.tweets.add(tweet)
        return HttpResponseRedirect('/user/' + username)


class HashTagCloud(View):
    """ Hash Tag page reachable from /hashtag/<hashtag> URL """

    def get(self, request, hashtag):
        params = dict()
        hashtag = HashTag.objects.get(name=hashtag)
        params["tweets"] = hashtag.tweets
        return render(request, 'hashtag.html', params)


class Search(View):
    """Search all tweets with query /search/?query=<query> URL"""

    def get(self, request):
        form = SearchForm()
        params = dict()
        params["search"] = form
        return render(request, 'search.html', params)

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            tweets = Tweet.objects.filter(text__icontains=query)
            context = Context({"query": query, "tweets": tweets})
            return_str = render_to_string('partials/_tweet_search.html', context)
            return HttpResponse(json.dumps(return_str), content_type="application/json")
        else:
            HttpResponseRedirect("/search")


class UserRedirect(View):
    def get(self, request):
        return HttpResponseRedirect('/user/'+request.user.username)


class MostFollowedUsers(View):
    def get(self, request):
        userFollower = UserFollowers.objects.order_by('-count')[:10] #list only the top 10 users
        params = dict()
        params['userFollowers'] = userFollower
        return render(request, 'users.html', params)


class Register(View):
    def get(self, request):
        params = dict()
        registration_form = RegisterForm()
        params['register'] = registration_form
        return render(request, 'registration/register.html', params)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)
            except:
                user = User(username=username, email=email)
                user.set_password(password)
                user.save()
                #user = super(user, self).save(commit=False)
                return HttpResponseRedirect('/login')
