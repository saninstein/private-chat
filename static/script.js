document.addEventListener("DOMContentLoaded", function () {
	main();
})

function main() {
	var input = document.getElementById('input')
	var chat = document.getElementById('chat')
	input.onkeyup = function (e) {
		if (e.keyCode == 13 && input.value.length) {
			console.log("Enter");
			sock.send(input.value)
		}
	}

	var sock = new WebSocket('ws://' + window.location.host + '/ws/' + chat.dataset.room);

	sock.onopen = function () {
		alert("Sock open!")
	}

	sock.onclose = function (e) {
		if (e.wasClean)
			console.log('Clean close')
		else
			console.log('Dirty close')
		console.log('Code: ' + e.code + ' reason: ' + e.reason)
	}

	sock.onmessage = function (e) {
		console.log(e.data)
		var data = JSON.parse(e.data)
		chat.innerHTML += data['msg'] + data['date_time'] + '<hr>'
	}

	sock.onerror = function (error) {
		console.log("Error: " + error.message)
	}
}
