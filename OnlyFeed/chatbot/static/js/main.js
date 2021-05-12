document.addEventListener('DOMContentLoaded', function () {
	document.getElementById("reload_message").addEventListener("click", add_message_user);
});

window.addEventListener("load", get_cookies)

var input = document.getElementById('send_message');
input.addEventListener('keydown', function (e) {
    if(e.keyCode==13) {
     add_message_user();
    }
});

function get_cookies(){
	$.ajax({
	url: '/get_cookies',
    type: 'POST',
    success: function (data) {
    	if(!data.message){
    		display_new_form()
    	}else{
    		display_all_messages(data.message)
    	}
        
    },
    error: function (data) {
        console.log("erreur")
    }});
}

function display_new_form(){
	document.getElementById("send_message").disabled = true
	document.getElementById("new_form").style.display = "block"
}

function display_message(message, type) {
	var get_messages = document.getElementById("messages");

	if(message != ''){
		var entry = document.createElement('li');
		if(type == 'user'){
			entry.classList.add("sent");
		}
		else if(type == 'chatbot'){
			entry.classList.add("replies");
		}
		entry.innerHTML+='<img src="http://emilcarlsson.se/assets/mikeross.png" alt="" />';
		entry.innerHTML+= '<p>'+message+'</p>';
		get_messages.appendChild(entry);
		document.getElementById("send_message").value = "";
	}
	
}

function add_message_user(){
	var message = document.getElementById("send_message").value;
	if(message != ""){
		$.ajax({
		url: '/add_user_message',
	    type: 'POST',
	    dataType: 'json',
	    data: { data: message},
	    success: function (data) {
	        display_message(message, 'user')
	    },
	    error: function (data) {
	        console.log(data.message)
	    }});
	}
}

function display_all_messages(email){
	console.log(email)
}