from django.shortcuts import render, redirect
import json
from django.views import View
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime
from itertools import groupby

class NewsView(View):
    def get(self, request, news_id, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, "r") as news_json:
            news_dict = json.load(news_json)
        for news in news_dict:
            if news["link"] == news_id:
                return render(request, "news/news.html", context={'news': news})

class NewsMainPageView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get("q")
        with open(settings.NEWS_JSON_PATH, "r") as news_json:
            news_dict = json.load(news_json)
        if q:
            news_dict = list(filter(lambda x: q in x["title"], news_dict))
        for news in news_dict:
            news["created"] = news["created"].split(" ")[0]
        news_dict.sort(key=lambda date: datetime.strptime(date["created"], "%Y-%m-%d"), reverse=True)
        news_dict_final = {}
        for key, group in groupby(news_dict, lambda news: news["created"]):
            news_dict_final[key] = list(group)
        return render(request, "news/index.html", context={'news': news_dict_final.items()})

class HomePageView(View):
    def get(self, request, *args, **kwargs):
        return redirect("/news/")

class CreateNewsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news/create.html")

    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        text = request.POST.get("text")
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(settings.NEWS_JSON_PATH, "r+") as news_json:
            news_dict = json.load(news_json)
            link = news_dict[-1]["link"] + 1
            new_news = {"created": created, "text": text, "title": title, "link": link}
            news_dict.append(new_news)
            news_json.seek(0)
            json.dump(news_dict, news_json)

        return redirect("/news/")

