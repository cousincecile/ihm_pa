document.addEventListener('DOMContentLoaded', function () {
	document.getElementById("reload_message").addEventListener("click", display_message);
});

var btn = document.getElementById('send_message');
btn.addEventListener('keydown', function (e) {
    if(e.keyCode==13) {
     display_message()
    }
});

function display_message() {
	
	var get_message = document.getElementById("send_message");
	var get_messages = document.getElementById("messages");

	if(get_message.value != ''){
		var entry = document.createElement('li');
		entry.classList.add("sent");
		entry.innerHTML+='<img src="http://emilcarlsson.se/assets/mikeross.png" alt="" />'
		entry.innerHTML+= '<p>'+get_message.value+'</p>';
		get_messages.appendChild(entry);
		get_message.value = "";
	}
	
}