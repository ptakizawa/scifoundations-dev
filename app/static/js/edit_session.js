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
				$('#themes').append('<option value="'+value+'">'+title+'</option>');
			});
			$.each(threads, function(index, value) {
				var title = value.replace(/-/g, ' ').replace(/\b./g, function(m){ return m.toUpperCase(); });
				$('#threads').append('<option value="'+value+'">'+title+'</option>');
			});
			$('#themes').change(function(e) {
				e.preventDefault();
				$('h2.theme-or-thread-title').empty();
				var theme = $(this).find('option:selected').attr('value');
				var title = theme.replace(/-/g, ' ').replace(/\b./g, function(m){ return m.toUpperCase(); });
				$('h2.theme-or-thread-title').append(title+' Sessions');
				list_session_by_theme(theme);
				
			});
			
			$('#threads').change(function(e) {
				e.preventDefault();
				$('h2.theme-or-thread-title').empty();
				var thread = $(this).find('option:selected').attr('value');
				var title = thread.replace(/-/g, ' ').replace(/\b./g, function(m){ return m.toUpperCase(); });
				$('h2.theme-or-thread-title').append(title+' Sessions');
			});
			
			$('#sessions-list').on('change', function(e) {
				e.preventDefault();
				var session_id = $(this).find('option:selected').attr('value');
				$.each(data['sessions'], function(index, value) {
					if (value['id'] == session_id) {
						var date = value['date-time'].split(' ')[0].split('-');
						var formatted_date = date[1] + '/' + date[2] + '/' + date[0]
						var time = value['date-time'].split(' ')[1];
						var hour = time.split(':')[0].replace(/^0+/,'');
						
						console.log(hour);						
						
						$('#session_id').val(value['id']);
						$('#title').val(value['title']);
						$('#pedagogy').val(value['pedagogy']);
						$('#thread').val(value['thread']);
						$('#theme').val(value['theme']);
						$('#summary').val(value['summary']);
						$('#datepicker').val(formatted_date);
						$('#time').val(hour);
					}
				});	
			});
			
			function list_session_by_theme(theme) {
				$('#sessions-list').empty();
				$('#sessions-list').append('<option></option>');
				$.each(data['sessions'], function(index, value) {
					if (value['theme'] == theme) {
						$('#sessions-list').append('<option value="'+value['id']+'">'+value['title']+'</option>');
					}					
				});
			}
			
			function list_session_by_thread(thread) {
				$('#sessions-list').empty();
				$('#sessions-list').append('<option></option>');
				$.each(data['sessions'], function(index, value) {
					if (value['thread'] == thread) {
						$('#sessions-list').append('<option value="'+value['id']+'">'+value['title']+'</option>');
					}					
				});
			}
		
		}
		
	});
});