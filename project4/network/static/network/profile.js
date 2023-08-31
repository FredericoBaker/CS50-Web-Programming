document.addEventListener('DOMContentLoaded', function() {
    let posts = document.querySelectorAll('#post-div');
    posts.forEach(element => {
        element.querySelector('.like').addEventListener('click', () => like_unlike(element));
    });
})

async function follow_unfollow(button) {
    const username = button.getAttribute('data-username');
    
    await fetch(`/follow/${username}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector("#follow-button").innerHTML = data.newStatus;
        document.querySelector("#user-followers").innerHTML = data.followers;
    });
}

function like_unlike(element) {

    const id = element.querySelector('#post-id').value;

    fetch('/like-post', {
        method: 'POST', 
        body: JSON.stringify({
            post_id: id,
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.liked) {
            element.querySelector('.like').classList.add('fa-heart');
            element.querySelector('.like').classList.remove('fa-heart-o');
        }
        else {
            element.querySelector('.like').classList.remove('fa-heart');
            element.querySelector('.like').classList.add('fa-heart-o');
        }
        element.querySelector("#likes-number").innerHTML = result.num_likes;
    })

}