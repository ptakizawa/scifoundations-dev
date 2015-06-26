$('document').ready(function(){
	$.ajax({
		type: 'GET',
		url: '/session-data',
		dataType: 'JSON',
		success: function(data) {
			var threads = data['threads']
			var themes = data['themes']
			$.each(themes, function(index, value) {
				var title = value.replace(/-/g, ' ').replace(/\b./g, function(m){ return m.toUpperCase(); });
				$('#theme').append('<option value="'+value+'">'+title+'</option>');
			});
			$.each(threads, function(index, value) {
				var title = value.replace(/-/g, ' ').replace(/\b./g, function(m){ return m.toUpperCase(); });
				$('#thread').append('<option value="'+value+'">'+title+'</option>');
			});
			$('#theme').change(function(e) {
				e.preventDefault();
				$('h2.theme-or-thread-title').empty();
				var theme = $(this).find('option:selected').attr('value');
				var title = theme.replace(/-/g, ' ').replace(/\b./g, function(m){ return m.toUpperCase(); });
				$('h2.theme-or-thread-title').append(title+' Sessions');
				list_session_by_theme(theme);
		
			});
	
			$('#thread').change(function(e) {
				e.preventDefault();
				$('h2.theme-or-thread-title').empty();
				var thread = $(this).find('option:selected').attr('value');
				var title = thread.replace(/-/g, ' ').replace(/\b./g, function(m){ return m.toUpperCase(); });
				$('h2.theme-or-thread-title').append(title+' Sessions');
				list_session_by_thread(thread);
			});
			
			function list_session_by_theme(theme) {
				$('#session').empty();
				$.each(data['sessions'], function(index, value) {
					if (value['theme'] == theme) {
						$('#session').append('<option value="'+value['id']+'">'+value['title']+'</option>');
					}					
				});
			}
			
			function list_session_by_thread(thread) {
				$('#session').empty();
				$.each(data['sessions'], function(index, value) {
					if (value['thread'] == thread) {
						$('#session').append('<option value="'+value['id']+'">'+value['title']+'</option>');
					}					
				});
			}
		}
	});
});