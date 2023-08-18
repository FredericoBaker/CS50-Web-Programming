document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view-email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Turn off default send form behaviour
  document.querySelector('#compose-form').addEventListener("submit", function(e) {
    e.preventDefault();
  }, true);

  // Send email functionality
  document.querySelector('#send-email-btn').addEventListener('click', send_email);
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = '';
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {

      const email_div = document.createElement('div');
      const read = email.read?'read':'unread';
      email_div.className = `${read} email-div`;
      email_div.innerHTML = `
        <div class="email-sender"><b>${mailbox==='sent'?email.recipients[0]:email.sender}</b></div>
        <div class="email-subject">${email.subject}</div>
        <div class="email-timestamp">${email.timestamp}</div>
      `;

      email_div.addEventListener('click', () => view_email(email.id));
      
      document.querySelector('#emails-view').appendChild(email_div); 
    });
  })

}

function send_email() {

  const recipients_value = document.querySelector('#compose-recipients').value;
  const subject_value = document.querySelector('#compose-subject').value;
  const body_value = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST', 
    body: JSON.stringify({
      recipients: `${recipients_value}`,
      subject: `${subject_value}`,
      body: `${body_value}`
    })
  })
  .then(response => response.json())
  .then(result => {

    if (typeof result.error !== 'undefined') {
      document.querySelector('#error-message').innerHTML = result.error;
    } 
    else {
      load_mailbox('sent')
    }

  })
}

function reply_email(id) {

  // Show the reply email view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view-email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#compose-recipients').value = `${email.sender}`;
    document.querySelector('#compose-subject').value = `${email.subject.split(' ')[0]==='Re:'?email.subject:'Re: ' + email.subject}`;
    document.querySelector('#compose-body').value = `\n\nOn ${email.timestamp + ' ' + email.sender} wrote: \n${email.body}`;
  })
  
  // Turn off default send form behaviour
  document.querySelector('#compose-form').addEventListener("submit", function(e) {
    e.preventDefault();
  }, true);

  // Send email functionality
  document.querySelector('#send-email-btn').addEventListener('click', send_email);
}

function view_email(id) {

  // Show the email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view-email').style.display = 'block';

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#from').innerHTML = `<b>From:</b> ${email.sender}`;
    document.querySelector('#to').innerHTML = `<b>To:</b> ${email.recipients}`;
    document.querySelector('#subject').innerHTML = `<b>Subject:</b> ${email.subject}`;
    document.querySelector('#timestamp').innerHTML = `<b>Timestamp:</b> ${email.timestamp}`;
    document.querySelector('#archive-email').innerHTML = `${email.archived?'Unarchive':'Archive'}`;
    document.querySelector('#body').innerHTML = `${email.body}`;

    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    })
    
    let archive_email = (id, archived) => {
      console.log('button clicked')
      if (archived) {

        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: false
          })
        })
        .then(response => response.json())
        .then(load_mailbox('inbox'))

      } 
      else {

        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: true
          })
        })
        .then(response => response.json())
        .then(load_mailbox('inbox'))

      }
    } 

    document.querySelector('#archive-email').addEventListener('click', () => archive_email(email.id, email.archived));
    document.querySelector('#reply-email').addEventListener('click', () => reply_email(email.id));

  });
}