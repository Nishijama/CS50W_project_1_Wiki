from cProfile import label
from random import randint
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django import forms
from markdown2 import Markdown
from . import util

markdowner = Markdown()


class NewEntryForm(forms.Form):
    new_title = forms.CharField(label="Entry title")
    new_body = forms.CharField(widget=forms.Textarea)

class EditEntryForm(forms.Form):
    edit_body = forms.CharField(widget=forms.Textarea)

def index(request):
    if request.method=="POST":
        search_data = request.POST.dict()
        search_term = search_data.get("q")
        # if entry with same title exists, redirect to that entry
        if util.get_entry(search_term):
            return HttpResponseRedirect(f"/wiki/{search_term}")
        # else redirect to search results
        else:
            return HttpResponseRedirect(f"/search_results/{search_term}")

    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def search_results(request, search_term):
    matching_results = []
    for entry in util.list_entries():
        if search_term.lower() in entry.lower():
            matching_results.append(entry)

    return render(request, "encyclopedia/search_results.html", {
        "search_term": search_term,
        "matching_results": matching_results
    })

def rand_entry(request):
    title = util.list_entries()[randint(0, len(util.list_entries())-1)]
    return render(request, "wiki/entry.html", {
        "random_entry": title
    })

def render_entry(request, title):
    if util.get_entry(title):
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(),
            "entry": markdowner.convert(util.get_entry(title))
        })
    else:
        return render(request, "encyclopedia/error.html", {
                    "error_title": "404. Page not found",
                    "error_description": "It looks like the page you're looking for does not exist"
                })

def new_entry(request):
    if request.method=="POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["new_title"]
            content = form.cleaned_data["new_body"]

            # if entry with same title already exists display error
            if util.get_entry(title):
                return render(request, "encyclopedia/error.html", {
                    "error_title": "XXX. Duplicate entry",
                    "error_description": "It looks like an entry with this title already exists"
                })

            # else create a new entry
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(f"/wiki/{title}")
        else:
            return render (request, "encyclopedia/new_entry.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/new_entry.html", {
            "form": NewEntryForm()
        })

def edit_entry(request, title):
    if request.method=="POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["edit_body"]

            util.save_entry(title, content)
            return HttpResponseRedirect(f"/wiki/{title}")
        else:
            return render (request, "encyclopedia/edit_entry.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/edit_entry.html", {
            "title": title.capitalize(),
            "form": EditEntryForm()
        })