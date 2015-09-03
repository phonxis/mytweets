#from django.core.serializers import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.template.loader import render_to_string
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from user_profile.models import User, UserFollowers
from tweets.models import Tweet, HashTag
from tweets.forms import TweetForm, SearchForm
import json


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
        userFollower = UserFollowers.objects.get(user=userProfile)
        if userFollower.followers.filter(username=request.user.username).exists():
            params["following"] = True
        else:
            params["following"] = False
        form = TweetForm(initial={'country': 'Global'})
        search_form = SearchForm()
        tweets = Tweet.objects.filter(user=userProfile).order_by('-created_date')
        params["tweets"] = tweets
        params["user"] = userProfile
        params["form"] = form
        params["search"] = search_form
        return render(request, 'profile.html', params)

    def post(self, request, username):
        follow = request.POST['follow']
        user = User.objects.get(username=request.user.username)
        userProfile = User.objects.get(username=username)
        userFollower, status = UserFollowers.objects.get_or_create(user=userProfile)
        if follow == "True":
            userFollower.followers.add(user)
        else:
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