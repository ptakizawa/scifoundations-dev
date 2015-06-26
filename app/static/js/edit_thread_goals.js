$('document').ready(function(){
	$.ajax({
		type: 'GET',
		url: '/thread-goals-data',
		dataType: 'JSON',
		success: function(data) {
			$.each(data, function(thread, goals) {
				var title = thread.replace(/-/g, ' ').replace(/\b./g, function(m){ return m.toUpperCase(); });
				$('#threads').append('<option value="'+thread+'">'+title+'</option>');
			});
			$('#threads').change(function(e) {
				e.preventDefault();
				$('h2.thread-title').empty();
				var thread = $(this).find('option:selected').attr('value');
				var title = thread.replace(/-/g, ' ').replace(/\b./g, function(m){ return m.toUpperCase(); });
				var thread_goals = data[thread];
				$('h2.thread-title').append(title);
				$.each(thread_goals, function(index, value) {
					$('form.form').append('<div class="form-group"><label for="'+value["id"]+'">Thread Goal:</label><textarea class="form-control" rows="5" name="'+value["id"]+'">'+value["goal"]+'</textarea>');					
				});
				$('form.form').append('<button type="submit" class="btn btn-default">Submit</button>');
			});
		
		}
	});
});