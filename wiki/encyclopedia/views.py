from django.shortcuts import render
import markdown2
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    markdownEntry = util.get_entry(entry)
    if markdownEntry:
        html = markdown2.markdown(markdownEntry)
    else:
        html = markdownEntry
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "content": html
    })