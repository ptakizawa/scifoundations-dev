$('document').ready(function(){
	var verbs;
	$.ajax({
		type: 'GET',
		url: '/session-data',
		dataType: 'JSON',
		success: function(data) {
			$.ajax({
				type: 'GET',
				url: '/verb-data',
				dataType: 'JSON',
				success: function(verb_data) {
					verbs = verb_data;
				}
			});
			
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
				list_session_by_thread(thread);
			});
			
			$('#sessions-list').on('change', function(e) {
				e.preventDefault();
				var session_id = $(this).find('option:selected').attr('value');
				$('#session_id').val(session_id);
			});
			
			$('#taxonomy').on('change', function(e) {
				e.preventDefault();
				$('#verb').empty();
				$('#verb').append('<option></option>');
				var taxonomy = $(this).find('option:selected').attr('value');
				var verb_list = verbs[taxonomy];
				verb_list.sort(function(a,b) {
					if (a['term'] > b['term']) {
						return 1;
					} else {
						return -1;
					}
				});
				$.each(verb_list, function(index, value) {
					$('#verb').append('<option value="'+ value['id'] +'">'+value['term']+'</option>');
					
				});
			});
			
			$('#who').on('change', function(e) {
				var who = $(this).find('option:selected').html();
				$('span.who').empty();
				$('span.who').append(who+ " should be able to ");
			});
			
			$('#verb').on('change', function(e) {
				var verb = $(this).find('option:selected').html();
				$('span.verb').empty();
				$('span.verb').append(verb + " ");
				var label_verb = verb.charAt(0).toUpperCase() + verb.substring(1);
				$('.content-label').html(label_verb + " what:");
			});
			
			$('#content').on('change', function(e) {
				e.preventDefault();
				$('span.content').html($(this).val() + " ");
			});
			
			$('#conditions').on('change', function(e) {
				e.preventDefault();
				$('span.conditions').html($(this).val() + ".");
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
				$.each(data['sessions'], function(index, value) {
					if (value['thread'] == thread) {
						$('#sessions-list').append('<option value="'+value['id']+'">'+value['title']+'</option>');
					}					
				});
			}
		
		}
		
	});
});