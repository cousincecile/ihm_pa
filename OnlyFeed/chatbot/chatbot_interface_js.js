function display_message() {
	var get_message = document.getElementById("send_message");
	var get_messages = document.getElementById("messages");
	get_messages.innerHTML+='<li class="sent">';
	get_messages.innerHTML+='<img src="http://emilcarlsson.se/assets/mikeross.png" alt="" />'
	get_messages.innerHTML+= '<p>'+get_message.value+'</p>';
	get_messages.innerHTML+= '</li>';
	get_message.value = "";
}

function get_input(){
	
}