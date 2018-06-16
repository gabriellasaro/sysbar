function submit_table(url){
	$.ajax({
		url: url,
		type: 'get',
		dataType: 'html',
		data: {
			'table':  $("#number").val()
		}
	}).done(function(data){
		data = JSON.parse(data)
		if (data.rStatus===0){
			console.log("Table not found.");
			document.getElementById('rStatus').style.display='block';
			document.getElementById('rStatus').innerHTML='Mesa não encontrada!';
		}else{
			console.log("Table set.");
			window.location.assign("/login/");
		}
	});
}

function submit_login(url){
	$.ajax({
		url: url,
		type: 'get',
		dataType: 'html',
		data: {
			'phone':  $("#login_name").val(),
			'pin':  $("#password").val()
		}
	}).done(function(data){
		data = JSON.parse(data)
		if (data.rStatus===11){
			console.log("Entrada não definida ou inválida!");
			document.getElementById('rStatus').style.display='block';
			document.getElementById('rStatus').innerHTML='Entrada não definida ou inválida!';
		}else if (data.rStatus===3){
			console.log("Usuário não encontrado!");
			document.getElementById('rStatus').style.display='block';
			document.getElementById('rStatus').innerHTML='Usuário não encontrado!';
		}else if (data.rStatus===4){
			console.log("Senha incorreta!");
			document.getElementById('rStatus').style.display='block';
			document.getElementById('rStatus').innerHTML='Senha incorreta!';
		}else{
			console.log("Conectado.");
			window.location.assign("/");
		}
	});
}

function submit_new(url){
	$.ajax({
		url: url,
		type: 'get',
		dataType: 'html',
		data: {
			'name':  $("#name").val(),
			'phone':  $("#icon_telephone").val(),
			'pin':  $("#password").val()
		}
	}).done(function(data){
		data = JSON.parse(data)
		if (data.rStatus===11){
			console.log("Entrada não definida ou inválida!");
			document.getElementById('rStatus').style.display='block';
			document.getElementById('rStatus').innerHTML='Entrada não definida ou inválida!';
		}else if (data.rStatus===9){
			console.log("Usuário já cadastrado/Telefone do usuário já está em uso!");
			document.getElementById('rStatus').style.display='block';
			document.getElementById('rStatus').innerHTML='Usuário já cadastrado/Telefone do usuário já está em uso!';
		}else if (data.rStatus===0){
			console.log("Erro ao enviar dados!");
			document.getElementById('rStatus').style.display='block';
			document.getElementById('rStatus').innerHTML='Erro ao enviar dados!';
		}else{
			console.log("Conta criada!");
			window.location.assign("/login/");
		}
	});
}