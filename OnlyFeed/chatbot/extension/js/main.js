var url = 'http://localhost:5001/'
var url_rasa = 'http://localhost:5005/webhooks/rest/webhook'
var userID

document.addEventListener('DOMContentLoaded', function () {
	document.getElementById("reload_message").addEventListener("click", add_message("from_user", 1));
});

window.addEventListener("load", get_cookies)

var input = document.getElementById('send_message');
input.addEventListener('keydown', function (e) {
    if(e.keyCode==13) {
     add_message("from_user", 1);
    }
});

var new_user_button = document.getElementById('new_user_button');
new_user_button.addEventListener("click", add_user)

function get_cookies(){
	chrome.cookies.get({ url: url, name: 'userID' },
		function (cookie) {
			if (cookie) {
			  userID = cookie.value
		      display_all_messages(cookie)
		    }
		    else {
		      display_new_form()
		    }
		});
}

function set_cookies(data){
	chrome.cookies.set({ url: url, name: "email", value: String(data.email) });
	chrome.cookies.set({ url: url, name: "username", value: String(data.username) });
	chrome.cookies.set({ url: url, name: "userID", value: String(data.id) });

	document.location.reload();
}

function display_new_form(){
	document.getElementById("send_message").disabled = true
	document.getElementById("new_form").style.display = "block"
}

function display_message(message, type) {
	var get_messages = document.getElementById("messages");

	if(message != ''){
		var entry = document.createElement('li');
		if(type == 1){
			entry.classList.add("sent");
		}
		else if(type == 0){
			entry.classList.add("replies");
		}
		entry.innerHTML+='<img src="http://emilcarlsson.se/assets/mikeross.png" alt="" />';
		entry.innerHTML+= '<p>'+message+'</p>';
		get_messages.appendChild(entry);
		document.getElementById("send_message").value = "";
		scroll_down()
	}
	
}

function add_user(){
	var email = document.getElementById("email").value
	var username = document.getElementById("username").value
	var age = document.getElementById("age").value

	$.ajax({
		url: url + 'add_user',
	    type: 'POST',
	    dataType: 'json',
	    data: { 
	    		email: email,
	    		username : username,
	    		age : age
	    	  },
	    success: function (data) {
	        set_cookies(data.message)
	    },
	    error: function (data) {
	        console.log(data.message)
	    }});
}

function add_message(message, type){

	if(message == "from_user"){
		message = document.getElementById("send_message").value;
	}

	if(message != ""){
		$.ajax({
		url: url + 'add_user_message',
	    type: 'POST',
	    dataType: 'json',
	    data: { 
	    		message: message,
	    		userID : userID,
	    		type : type
	    	  },
	    success: function (data) {
	    	if(type == 1){
	    		query_rasa(message)
	    	}
	        display_message(message, type)
	    },
	    error: function (data) {
	        console.log(data.message)
	    }});
	}
}

function scroll_down(){
	var chat_div = document.getElementById("chat_window")
	chat_div.scrollTop = chat_div.scrollHeight
}

function display_all_messages(){

	$.ajax({
		url: url + 'get_all_messages',
	    type: 'POST',
	    dataType: 'json',
	    data: {
	    		userID : userID
	    	  },
	    success: function (data) {
	    	messages = data.message
	    	for (var i = 0; i < messages.length; i++){
	    		display_message(messages[i].content, messages[i].type)
	    	}
	    },
	    error: function (data) {
	        console.log(data.message)
	    }});
}

function query_rasa(message, useriD){

	console.log(message)

	$.ajax({
		url: url_rasa,
	    type: 'POST',
	    dataType: 'json',
	    data:JSON.stringify({
	    		sender: userID,
	    		message: message
	    	  }),
	    success: function (data) {
	    	for (var i = 0; i < data.length; i++){
	    		add_message(data[i].text, 0)
	    	}
	    },
	    error: function (data) {
	        console.log(data)
	    }});

}

