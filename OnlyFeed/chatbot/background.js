document.addEventListener('DOMContentLoaded', function () {
	document.getElementById("reload_message").addEventListener("click", display_message);
});

var btn = document.getElementById('send_message');
btn.addEventListener('keydown', function (e) {
    if(e.keyCode==13) {
     display_message("user");
    }
});

function display_message(message_type, message="") {

	var get_messages = document.getElementById("messages");

	if (message_type == "user"){
		var get_message = document.getElementById("send_message");
		if(get_message.value != ''){
			var entry = document.createElement('li');
			entry.classList.add("sent");
			entry.innerHTML+='<img src="http://emilcarlsson.se/assets/mikeross.png" alt="" />';
			entry.innerHTML+= '<p>'+get_message.value+'</p>';
			get_messages.appendChild(entry);
			get_message.value = "";
		}

		//Enregistrer message dans bdd (appel fonction backend)
		//Réponse du chatbot 
			// => display_message('chatbot', message)



	}else if(message_type == "chatbot"){
		var entry = document.createElement('li');
			entry.classList.add("replies");
			entry.innerHTML+='<img src="http://emilcarlsson.se/assets/mikeross.png" alt="" />';
			entry.innerHTML+= '<p>bip boup je suis le chatbot</p>';
			get_messages.appendChild(entry);
			get_message.value = "";
	}

	
}