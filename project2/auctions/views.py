from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing, Category, Bid, Comment
from .forms import CreateListingForm, CreateComment


def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="login")
def newListing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            auctionListing = AuctionListing(user= request.user, 
                                            title=form.cleaned_data["title"], 
                                            description=form.cleaned_data["description"],
                                            image=form.cleaned_data["image"], 
                                            currentPrice=form.cleaned_data["currentPrice"], 
                                            open=True,
                                            category=Category.objects.get(pk=form.cleaned_data["category"].id))
            auctionListing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = CreateListingForm()
    return render(request, "auctions/new-listing.html", {
        "form": form,
        "categories": Category.objects.all()
    })

def listing(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    isCreator = listing.user == request.user
    isLoggedIn = request.user.is_authenticated
    inWatchlist = isLoggedIn and request.user.watchlist.filter(pk=listing_id).exists()
    currentWinner = listing.currentBid is not None and request.user == listing.currentBid.user
    commentForm = CreateComment()
    
    if request.method == "POST":
        if request.POST["operation"] == "remove-watchlist":
            request.user.watchlist.remove(listing)
            inWatchlist = True
        
        elif request.POST["operation"] == "add-watchlist":
            request.user.watchlist.add(listing)
            inWatchlist = False
        
        elif request.POST["operation"] == "close-auction" and isCreator:
            listing.open = False
            listing.save()

        elif request.POST["operation"] == "comment":
            commentForm = CreateComment(request.POST)
            if commentForm.is_valid():
                newComment = Comment(auction=listing,
                                     user=request.user,
                                     text=commentForm.cleaned_data["text"])
                newComment.save()
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

        elif request.POST["operation"] == "bid":
            if listing.currentBid is None and int(request.POST["bid"]) == listing.currentPrice or listing.currentBid is not None and int(request.POST["bid"]) > listing.currentPrice:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "isCreator": isCreator,
                    "isLoggedIn": isLoggedIn,
                    "inWatchlist": inWatchlist,
                    "userHasLastBid": listing.currentBid is not None and listing.currentBid.user == request.user,
                    "numberOfBids": listing.bids.count(),
                    "currentWinner": currentWinner,
                    "comments": listing.comments.all(),
                    "commentForm": commentForm,
                    "message": "Your bid must be greater than the current bid."
                })
            bid = Bid(auction=listing, 
                      user=request.user,
                      value=int(request.POST["bid"]))
            bid.save()
            listing.currentBid = bid
            listing.currentPrice = int(request.POST["bid"])
            listing.save()
        
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "isCreator": isCreator,
        "isLoggedIn": isLoggedIn,
        "inWatchlist": inWatchlist,
        "userHasLastBid": listing.currentBid is not None and listing.currentBid.user == request.user,
        "numberOfBids": listing.bids.count(),
        "currentWinner": currentWinner,
        "comments": listing.comments.all(),
        "commentForm": commentForm
    })

@login_required(login_url="login")
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "listings": request.user.watchlist.all()
    })

def category(request):
    if request.method == "GET":       
        return render(request, "auctions/category.html", {
            "categories": Category.objects.all(),
            "listings": AuctionListing.objects.filter(category=request.GET.get('category'))
        })
    return render(request, "auctions/category.html", {
        "categories": Category.objects.all()
    })