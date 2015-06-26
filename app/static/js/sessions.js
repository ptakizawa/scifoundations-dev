$('document').ready(function(){
	$.ajax({
		type: 'GET',
		url: '/session-data',
		dataType: 'JSON',
		success: function(data) {
			console.log(data);
			var threads = data['threads']
			var themes = data['themes']
			$.each(themes, function(index, value) {
				var title = value.replace(/-/g, ' ').replace(/\b./g, function(m){ return m.toUpperCase(); });
				$('#themes').append('<option value="'+value+'">'+title+'</option>');
			});
			$.each(threads, function(index, value) {
				var title = value.replace(/-/g, ' ').replace(/\b./g, function(m){ return m.toUpperCase(); });
				$('#threads').append('<option value="'+value+'">'+title+'</option>');
			});
			$('#themes').change(function(e) {
				e.preventDefault();
				$('#sessions').empty();
				var theme = $(this).find('option:selected').attr('value');
				var title = theme.replace(/-/g, ' ').replace(/\b./g, function(m){ return m.toUpperCase(); });
				$('#sessions').append('<h2>'+title+' Sessions</h2>');
				$('#sessions').append('<ul class="sessions-list"></ul>');
				$.each(data['sessions'], function(index, session) {
					if (session['theme'] == theme) {
						$('.sessions-list').append('<li>'+session['title']+'</li>');						
					}
				});
			});
			
			$('#threads').change(function(e) {
				e.preventDefault();
				$('#sessions').empty();
				var thread = $(this).find('option:selected').attr('value');
				var title = thread.replace(/-/g, ' ').replace(/\b./g, function(m){ return m.toUpperCase(); });
				$('#sessions').append('<h2>'+title+' Sessions</h2>');
				$('#sessions').append('<ul class="sessions-list"></ul>');
				$.each(data['sessions'], function(index, session) {
					if (session['thread'] == thread) {
						$('.sessions-list').append('<li>'+session['title']+'</li>');						
					}
				});
			});
		
		}
	});
});