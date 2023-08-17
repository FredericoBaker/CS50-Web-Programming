from django import forms
from .models import *

class CreateListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ["title", "description", "image", "currentPrice", "category"]

    def __init__(self, *args, **kargs):
        super(CreateListingForm, self).__init__(*args, **kargs)
        self.fields['title'].widget.attrs.update({"class": "form-control", "placeholder": "Title"})
        self.fields['description'].widget.attrs.update({"class": "form-control", "placeholder": "Description", "rows": 3})
        self.fields['image'].widget.attrs.update({"class": "form-control", "placeholder": "Image link"})
        self.fields['currentPrice'].widget.attrs.update({"class": "form-control", "placeholder": "Starting Bid"})
        self.fields['category'].widget.attrs.update({"class": "form-control", "placeholder": "Category"})

class CreateComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]

    def __init__(self, *args, **kargs):
        super(CreateComment, self).__init__(*args, **kargs)
        self.fields['text'].widget.attrs.update({"class": "form-control", "placeholder": "Write your comment", "rows": 3})