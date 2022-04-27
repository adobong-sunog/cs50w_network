document.addEventListener('DOMContentLoaded', function() {

  document.querySelector('#make').addEventListener('click', show_form);

});

function all_posts () {

  fetch('')
  .then(response => {
    console.log('went to all-posts')
  });

}

// Get csrf token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

// Show 'make post' form
function show_form () {

  let button = document.querySelector('#make-post');
  document.querySelector('#img').value = '';
  document.querySelector('#txt').value = '';
  if (button.classList.contains('on')) {
    button.classList.remove('on');
  }
  else {
    button.classList.add('on')
  }
}

// Show edit form
function edit_form (formid) {
   
  let eform = document.querySelector(`#editform${formid}`);
  document.querySelector('#editimg').value = '';
  document.querySelector('#edittxt').value = '';

  if (eform.classList.contains('on')) {
    eform.classList.remove('on');
  }
  else {
    eform.classList.add('on')
  }
}

// Create or edit post
function make_post (opt) {
  
  var choice = 'cs50 is an amazing course';
  if (opt === 'Post') {
    console.log('tried to make a post');
    choice = 'post';

    const image = document.querySelector('#img').value;
    const text = document.querySelector('#txt').value;
    const sender = document.querySelector('#sender').value;

    fetch('/make-post', {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        "X-CSRFToken": getCookie("csrftoken")
      },
      body: JSON.stringify({
        image: image,
        text: text,
        sender: sender,
        choice: choice
      })
    })
    .then(response => response.json())
    .then(created => {
      console.log(created);
      all_posts();
      location.reload()
    });
  }
  else if (opt === 'Edit'){
    console.log('tried to edit a post');
    choice = 'edit';

    const editimage = document.querySelector('#editimg').value;
    const edittext = document.querySelector('#edittxt').value;
    const postid = document.querySelector('#thesender').value;
    var eform = document.querySelector(`#editform${postid}`);

    // 'Close' edit form after submission
    if (eform.classList.contains('on')) {
      eform.classList.remove('on');
    }
    else {
      eform.classList.add('on')
    }

    fetch('/make-post', {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        "X-CSRFToken": getCookie("csrftoken")
      },
      body: JSON.stringify({
        image: editimage,
        text: edittext,
        postid: postid,
        choice: choice
      })
    })
    .then(response => response.json())
    .then(result => {
      document.querySelector(`#currenttxt${postid}`).innerHTML = result.newtxt;

      // Check if there's a new image to prevent null error
      if (result.newimg != null) {
        document.querySelector(`#currentimg${postid}`).src = `${result.newimg}`;
      }
    })
  }
  else {
    return console.log("post option error");
  }
}

function to_follow (option) {

  console.log('followed');

  const followed = document.querySelector('#the_followed').value;
  const follower = document.querySelector('#the_follower').value;

  // Check if the button value is 'follow' or 'unfollow'.
  var check = 'cs50w is also an amazing course'
  if (option === 'follow') {
    check = 'follow'
  }
  else if (option === 'unfollow') {
    check = 'unfollow'
  }
  else {
    return console.log("Value error");
  }

  fetch('/follow', {
    method: 'POST',
    credentials: 'same-origin',
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    body: JSON.stringify({
      followed: followed,
      follower: follower,
      check: check
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
    location.reload();
    return false;
  })

}

function add_like (postid, userid) {
  
  var likenum = document.querySelector(`#likes${postid}`);

  fetch('/like', {
    method: 'POST',
    body: JSON.stringify({
      postid: postid,
      userid: userid
    })
  })
  .then((response) => response.json())
  .then((response) => {
    if (response.status === 201) {
      likenum.innerHTML = response.numlikes;
    }
    else {
      return console.log("No response");
    }
  })
}