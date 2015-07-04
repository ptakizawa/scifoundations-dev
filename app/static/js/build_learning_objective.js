$('document').ready(function(){
    $(document).tooltip();
    $.ajax({
        type: 'GET',
        url: '/verb-data',
        dataType: 'JSON',
        success: function(verb_data) {
            var verbs = verb_data;
            if ($('#who').find('option:selected').html() != '') {
                var who = $('#who').find('option:selected').html();
                $('span.who').empty();
                $('span.who').append(who+ " should be able to ");
            }
            
            $('#who').on('change', function(e) {
                var who = $(this).find('option:selected').html();
                $('span.who').empty();
                $('span.who').append(who+ " should be able to ");
            });
            
            if ($('#taxonomy').find('option:selected').html() != '') {
                var taxonomy = $('#taxonomy').find('option:selected').attr('value');
                $('#verb').empty();
                $('#verb').append('<option></option>');
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
            }
            
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
            
            if ($('#verb').find('option:selected').html != '') {
                var verb = $('#verb').find('option:selected').html();
                $('span.verb').empty();
                $('span.verb').append(verb + " ");
                var label_verb = verb.charAt(0).toUpperCase() + verb.substring(1);
                //$('.content-label').html(label_verb + " what:");
            }
    
            $('#verb').on('change', function(e) {
                var verb = $(this).find('option:selected').html();
                $('span.verb').empty();
                $('span.verb').append(verb + " ");
                var label_verb = verb.charAt(0).toUpperCase() + verb.substring(1);
                $('.content-label').html(label_verb + " what:");
            });
    
            $('#content').on('change', function(e) {
                var content = $(this).val();
                $('span.content').html(content.charAt(0).toLowerCase() + content.substring(1) + ".");
            });
    
            $('#conditions').on('change', function(e) {
                e.preventDefault();
                if ($(this).val() != '') {
                    var conditions = $(this).val();
                    $('span.conditions').html(conditions.charAt(0).toUpperCase() + conditions.substring(1) + ", ");
                    var who = $('span.who').html();
                    $('span.who').html(who.charAt(0).toLowerCase() + who.substring(1));
                } else {
                    $('span.conditions').html($(this).val());
                    var who = $('span.who').html();
                    $('span.who').html(who.charAt(0).toUpperCase() + who.substring(1));
                }
            });
        }
        
    });
});