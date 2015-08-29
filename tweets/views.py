#from django.core.serializers import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.template.loader import render_to_string
from django.views.generic import View
from user_profile.models import User
from tweets.models import Tweet, HashTag
from tweets.forms import TweetForm, SearchForm
import json


# Create your views here.


class Index(View):
    def get(self, request):
        params = {"name": "Django", "version": "1.8"}
        return render(request, 'base.html', params)

    def post(self):
        return HttpResponse('post request')


class Profile(View):
    """	User profile page reachable from /user/<username> URL	"""

    def get(self, request, username):
        # params = dict()()() i dont know that this mean
        params = {}
        user = User.objects.get(username=username)
        tweets = Tweet.objects.filter(user=user)
        params["tweets"] = tweets
        params["user"] = user
        return render(request, 'profile.html', params)


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