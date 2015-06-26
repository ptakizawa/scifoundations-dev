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
				$('#thread-goals').empty();
				var thread = $(this).find('option:selected').attr('value');
				var title = thread.replace(/-/g, ' ').replace(/\b./g, function(m){ return m.toUpperCase(); });
				var thread_goals = data[thread];
				$('#thread-goals').append('<h2>'+title+'</h2><ul class="goals-list"></ul>')
				$.each(thread_goals, function(index, value) {
					$('ul.goals-list').append('<li>'+value["goal"]+'</li>');						
				});
			});
		
		}
	});
});