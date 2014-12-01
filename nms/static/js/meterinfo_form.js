fetchStrings = function (well_pk){
    strings_json_url = $('#strings_json_url').data('url')
    console.log(strings_json_url)
    $.getJSON(strings_json_url, {'well': well_pk}, function(data){
	    console.log(data)
	    if(data.length > 0){
		var options = '';
		for(var i = 0; i < data.length; i++){
		    options += '<option value="' + data[i].pk + '">' + data[i].number + '</option>';
		}
		$('#id_string').html(options);
	    } else {
		$('#id_string').empty()
	    }
	})
}

updateDropDown = function(){
    well_pk = $('#id_well').val()
    if(well_pk){
	fetchStrings(well_pk)
    }
}
updateDropDown();
$('#id_well').change(updateDropDown);

