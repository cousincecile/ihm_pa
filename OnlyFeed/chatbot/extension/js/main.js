var url = 'http://localhost:5000/'
var url_rasa = 'http://localhost:5005/webhooks/rest/webhook'
var userID
var id_game
var latest_chatbot_message = 0

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

var new_user_button = document.getElementById('new_comparison_form');
new_user_button.addEventListener("click", add_user)

function add_user_comparison(){
	var select_value = document.getElementById("select_game").value

	if(select_value == ""){
		return
	}

	$.ajax({
		url: url + 'get_comparison_result',
	    type: 'POST',
	    dataType: 'json',
	    data: { 
	    		userID : userID,
	    		gameID : id_game,
	    		result : select_value
	    	  },
	    success: function (data) {
	    	message = "Merci de ta réponse, je m'améliore grace à toi !"
	    	type = 0
	    	add_message(message, type)
	        document.location.reload();
	    },
	    error: function (data) {
	        console.log(data.message)
	    }});


}

function display_comparison_form(message){
	document.getElementById("send_message").disabled = true
	document.getElementById("comparison_form").style.display = "block"
	comparison_form = document.getElementById("comparison_form")
	var title = document.createElement("H2")
	title.classList.add("title_form")
	
	
	for(key in message.test_game) {
    	var t = document.createTextNode("Lequel de ces jeux se rapprochent le plus de " + message.test_game[key]);
    	title.appendChild(t)
    	id_game = key
	}

	comparison_form.appendChild(title)

	var select = document.createElement("select");
	select.id = "select_game";

	for (i = 1; i <= 3; i += 1){
		var name = "game" + i
		for(key in message[name]) {
			var option = document.createElement("option");
			option.value = i - 1
		    option.text = message[name][key];
		    select.appendChild(option);
		}
	}

	var aucun = document.createElement("option");
	aucun.value = 3
	aucun.text = "Aucun";
	select.appendChild(aucun);

	var unknown = document.createElement("option");
	unknown.value = 4
	unknown.text = "Je ne sais pas"
	select.appendChild(unknown);

	select.classList.add("form-select")

	comparison_form.appendChild(select)

	var submit_button_comparison = document.createElement("button")
	submit_button_comparison.classList.add("btn")
	submit_button_comparison.id = "submit_button_comparison"
	submit_button_comparison.innerHTML = "Envoyer"

	comparison_form.appendChild(submit_button_comparison)
	submit_button_comparison.addEventListener("click", add_user_comparison)
}

function get_game_comparison(id_user){
	$.ajax({
		url: url + 'get_comparison',
	    type: 'POST',
	    dataType: 'json',
	    data: { 
	    		userID : id_user
	    	  },
	    success: function (data) {
	        if(data.message == 0){
	        	display_all_messages()
	        }else{
	        	display_comparison_form(data.message)
	        }
	    },
	    error: function (data) {
	        console.log(data.message)
	    }});
}

function get_cookies(){
	chrome.cookies.get({ url: url, name: 'userID' },
		function (cookie) {
			if (cookie) {
			  userID = cookie.value
			  get_game_comparison(userID)
		    }
		    else {
		      display_new_form()
		    }
		});
}

function set_cookies(data){
	chrome.cookies.set({ url: url, name: "email", value: String(data.email), expirationDate: (new Date().getTime()/1000) + 2628000 });
	chrome.cookies.set({ url: url, name: "username", value: String(data.username), expirationDate: (new Date().getTime()/1000) + 2628000 });
	chrome.cookies.set({ url: url, name: "userID", value: String(data.id), expirationDate: (new Date().getTime()/1000) + 2628000 });

	document.location.reload();
}

function display_new_form(){
	document.getElementById("send_message").disabled = true
	document.getElementById("new_form").style.display = "block"
}

function display_message(message, type) {
	var get_messages = document.getElementById("messages");

	if(message != ''){

		if(message.localeCompare("Entrez une note entre 1 et 10", 'fr', { sensitivity: 'base' }) == 0 && type == 1){
			latest_chatbot_message = 1
		}

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

function add_message(message, type, check_answer = 0){

	if(check_answer == 1){
		latest_chatbot_message = 1
	}

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
	    	if(type == 1 && latest_chatbot_message == 0){
	    		query_rasa(message)
	    	}
	        display_message(message, type)
	    },
	    error: function (data) {
	        console.log(data.message)
	    }});


		if(latest_chatbot_message == 1 && type == 1){
			latest_chatbot_message = 0
			if(isNaN(message)){
				add_message("Entrez une note entre 1 et 10", 0, 1)
			}

			else{
				console.log(parseInt(message))
			 	if(parseInt(message) < 1){
					add_message("Entrez une note entre 1 et 10", 0, 1)
				}

				if(parseInt(message) > 10){
					add_message("Entrez une note entre 1 et 10", 0, 1)
				}
			}

		}
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
	    		if(data[i].text.localeCompare("Notez cette recommandation entre 1 et 10", 'fr', { sensitivity: 'base' }) == 0){
	    			latest_chatbot_message = 1
	    		}
	    		add_message(data[i].text, 0)
	    	}
	    },
	    error: function (data) {
	        console.log(data)
	    }});

}