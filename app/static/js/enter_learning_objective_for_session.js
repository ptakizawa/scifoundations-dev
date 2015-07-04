$('document').ready(function() {
    $.ajax({
		type: 'GET',
		url: '/session-data',
		dataType: 'JSON',
		success: function(data) {
			var threads = data['threads']
			var themes = data['themes']

			$('#theme').change(function(e) {
				e.preventDefault();
				var theme = $(this).find('option:selected').attr('value');
				list_session_by_theme(theme);
				
			});
			
			$('#thread').change(function(e) {
				e.preventDefault();
				var thread = $(this).find('option:selected').attr('value');
				list_session_by_thread(thread);
			});
			
			$('#session').change(function(e) {
			    e.preventDefault();
			    var session = $(this).find('option:selected').attr('value');
			    $('#session_id').val(session);
			});
			
			function list_session_by_theme(theme) {
				$('#session').empty();
				$('#session').append('<option></option>');
				$.each(data['sessions'], function(index, value) {
					if (value['theme'] == theme) {
						$('#session').append('<option value="'+value['id']+'">'+value['title']+'</option>');
					}					
				});
			}
			
			function list_session_by_thread(thread) {
				$('#session').empty();
				$('#session').append('<option></option>');
				$.each(data['sessions'], function(index, value) {
					if (value['thread'] == thread) {
						$('#session').append('<option value="'+value['id']+'">'+value['title']+'</option>');
					}					
				});
			}
		}
	});

});