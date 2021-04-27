function display_message() {
	var get_message = document.getElementById("send_message");
	var get_messages = document.getElementById("messages");
	get_messages.innerHTML+='<div class="vicbot"><img class="pic_bot" src="vicbot.jfif">';
	get_messages.innerHTML+= '<p>'+get_message.value+'</p>';
	get_messages.innerHTML+= '</div>';
	get_message.value = "";
	console.log(get_message);
}