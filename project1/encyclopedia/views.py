from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import path
from django import forms

from random import seed
from random import randint

import markdown2
from . import util

seed(1)

class NewArticleForm(forms.Form):
    title = forms.CharField(label = "Article title", 
                            widget = forms.TextInput(attrs = {'style': 'max-width: 600px;', 
                                                              'class': 'form-control'}))
    content = forms.CharField(label = "Article content", 
                              widget = forms.Textarea(attrs = {'rows': 1, 
                                                               'cols': 1, 
                                                               'style': 'max-width: 600px; min-height: 300px', 
                                                               'class': 'form-control'}))

class NewEditForm(forms.Form):
    content = forms.CharField(label = "Article content", 
                              widget = forms.Textarea(attrs = {'rows': 1, 
                                                               'cols': 1, 
                                                               'style': 'max-width: 600px; min-height: 300px', 
                                                               'class': 'form-control'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, name):
    markdownEntry = util.get_entry(name)
    if markdownEntry:
        html = markdown2.markdown(markdownEntry)
    else:
        html = markdownEntry
    return render(request, "encyclopedia/article.html", {
        "title": name,
        "content": html
    })

def search(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        entries = util.list_entries()
        queryList = []
        for entry in entries:
            if query.lower() == entry.lower():
                return redirect("article", name=query)
            elif query.lower() in entry.lower():
                queryList.append(entry)
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "results": queryList
        })

def new(request):
    if request.method == "POST":
        form = NewArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is None:
                with open(f'entries/{title}.md', 'w') as file:
                    file.write(content)
                return redirect("article", name=title)
            else:
                return render(request, "encyclopedia/new.html", {
                    "error": "This article already exists.",
                    "form": form
                })
    else:
        form = NewArticleForm()

    return render(request, "encyclopedia/new.html", {
        "form": form
    })

def edit(request, name):
    if request.method == "POST":
        form = NewEditForm(request.POST)
        if form.is_valid():
            newContent = form.cleaned_data["content"]
            with open(f'entries/{name}.md', 'w') as file:
                file.write(newContent)
            return redirect("article", name=name)
    else:
        curContent = util.get_entry(name)
        form = NewEditForm({
            "content": curContent
        })

    return render(request, "encyclopedia/edit.html", {
                    "form": form,
                    "title": name
                })

def random(request):
    articlesList = util.list_entries()
    randomInt = randint(0, len(articlesList) - 1)
    return redirect("article", name=articlesList[randomInt])