
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#new-post-form').addEventListener("submit", (e) => new_post(e));

    let posts = document.querySelectorAll('#post-div');
    posts.forEach(element => {
        element.querySelector('.like').addEventListener('click', () => like_unlike(element));
    });
})

function hide(id) {

    const element = document.querySelector(id);
        
    if (element.style.display === "block") {
        setTimeout(() => {
            element.style.display = "none";
        }, 5000);
    }

}

function new_post(e) {
    e.preventDefault();

    const content = document.querySelector('#content').value;

    fetch('./create-post', {
        method: 'POST', 
        body: JSON.stringify({
            content: `${content}`,
        })
    })
    .then(response => response.json())
    .then(result => {

        if (typeof result.error !== 'undefined') {
            document.querySelector('#content').value = "";
            document.querySelector('#error').innerHTML = result.error;
            document.querySelector('#error').style.display = "block";
            hide("#error");
        }
        else {
            document.querySelector('#content').value = ""; 
            document.querySelector('#success').innerHTML = result.message;
            document.querySelector('#success').style.display = "block";
            add_post(content);
            hide("#success");
        }

    })

}

function add_post(content) {
    const div = document.createElement('div');
    div.classList.add('container-template');
    div.setAttribute('id', 'post');

    const timestamp = new Date().toLocaleString();
    const username = JSON.parse(document.getElementById('username').textContent);

    div.innerHTML = `
    <div id="post-header">
        <a id="post-username" href="profile/${username}">${username}</a>
        <a href="" id="post-edit">Edit</a>
    </div>
    <p id="post-content">${content}</p>
    <p id="post-timestamp">${timestamp}</p>
    <div id="post-likes">
        <i class="fa fa-heart" id="likes-icon"></i>
        <span id="likes-number">0</span>
    </div>
    <p id="post-comment">Comment</p>
    `;

    document.querySelector('#posts').prepend(div);
}

function edit_post(id) {

    document.querySelector(`#content-post-${id}`).style.display = "none";
    document.querySelector(`#edit-post-${id}`).style.display = "block";

    document.querySelector(`#edit-post-${id}`).addEventListener("submit", (e) => {
        e.preventDefault()
        
        const content = document.querySelector(`#content-${id}`).value;

        fetch('./edit-post', {
            method: 'POST', 
            body: JSON.stringify({
                post_id: id,
                content: content,
            })
        })
        .then(response => response.json())
        .then(result => {
            document.querySelector(`#edit-post-${id}`).style.display = "none";
            document.querySelector(`#content-post-${id}`).innerHTML = content;
            document.querySelector(`#content-post-${id}`).style.display = "block";
        })

    });
}

function like_unlike(element) {

    const id = element.querySelector('#post-id').value;

    fetch('./like-post', {
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
