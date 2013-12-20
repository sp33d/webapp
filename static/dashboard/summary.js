var summaryTable;
var csvData = [['No Data']];

$(document).ready(function() {
    $('#summaryTableContainer').html( '<table cellpadding="0" cellspacing="0" border="0" class="table table-striped table-bordered" id="summaryTable"></table>' );
    summaryTable = $('#summaryTable').dataTable( {
        "bPaginate": true,
        "bFilter": true,
        "bSort": true,
        /* Disable initial sort */
        "aaSorting": [],
        "bAutoWidth": false, 
        "aoColumns": [
            { "sTitle": "Name" },
            { "sTitle": "Location" },
            { "sTitle": "Status" },
            { "sTitle": "Fuel" },
            { "sTitle": "Mileage" },
            { "sTitle": "Time" }
        ]
    } );
    
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    loadSummary();
    var sec_60 = 60 * 1000;
    setInterval(function(){loadSummary();},sec_60);
    //setInterval(function(){refreshFilesSettings();},sec_30);
});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


function alertBox(title, msg, ok_cancel, action_html){
    $('#alertModalBoxTitle').html(title);
    $('#alertModalBoxBody').html('<p>' + msg + '</p>');
    if( ok_cancel ) {
        $('#alertModalBoxFooter').html(action_html);      
    }
    $('#alertModalBox').modal();
}


function downloadCSV(){
    var csvContent = csvData;
    var csvstring="";
    for(record_index in csvContent){
        first = true
        for(feild_index in csvContent[record_index]){
            if(first){
                csvstring += '"' + csvContent[record_index][feild_index] + '"';
                first=false;
            }else{
                csvstring += ',"' + csvContent[record_index][feild_index] + '"';
            }
        }
        csvstring += "\n";
    }
    console.log(csvstring);
    /*var w = window.open('','csvWindow');
    //w.document.open("text/csv");
    w.document.writw('<meta name="content-type" content="text/csv">');
    w.document.write('<meta name="content-disposition" content="attachment;  filename=data.csv">');
    w.document.write(csvstring); 
    //w.document.close();
    //navigator.msSaveBlob(blob, "live-summary.csv");*/
    var a = document.createElement('a');
    a.href     = 'data:attachment/csv,' + encodeURIComponent(csvstring);
    a.target   = '_blank';
    a.download = 'live-summary-'+ local_time_as_file_name() +'.csv';
    document.body.appendChild(a);
    a.click(); 
}

function loadSummary(did, divn) {
    $('#summaryStatus').html('<img src="/static/images/ajax_loader_blue_350.gif" height="10px" width="10px"/>');
    $.ajax({
            url: "/dashboard/ajax/summary/",
            data: {'did': did},
            type: "POST"
    }).done(function(data){
            summaryTable.fnClearTable();
            //summaryTable.fnDestroy();
            if(data['status'] == 'ok'){
                records = data['summary'];
                csvData = [['S No','ID', 'Name','Address','Power','Ignition','GPS Signal','Fuel','Mileage','Time']]
                for(var i=0; i<records.length; i++)
                {
                    var row = [];
                    var csvRow = []
                    if(records[i]['packet'] == null){
                      row = [
                                records[i]['name'],
                                '',
                                '',
                                '',
                                '',
                                ''
                            ];
                        csvRow = [
                                    i+1,
                                    records[i]['imei'],
                                    records[i]['name'],
                                    'N/A',
                                    'N/A',
                                    'N/A',
                                    'N/A',
                                    'N/A',
                                    'N/A',
                                    'N/A'
                                ];
                    }else{
                      //data is available
                        row = [ 
                                records[i]['name'],
                                records[i]['packet']['address'],
                                '' + get_power_icon(records[i]['packet']['ps']) + '' +
                                '' + get_ig_icon(records[i]['packet']['ig']) + '' +
                                '' + get_gps_icon(records[i]['packet']['signal']) + '',
                                records[i]['packet']['fuel'],
                                records[i]['packet']['mileage'],
                                getFormattedDateLocal(records[i]['time'])
                            ];
                        csvRow = [
                                    i+1,
                                    records[i]['imei'],
                                    records[i]['name'],
                                    records[i]['packet']['address'],
                                    get_power_text(records[i]['packet']['ps']),
                                    get_ig_text(records[i]['packet']['ig']),
                                    get_gps_text(records[i]['packet']['signal']),
                                    records[i]['packet']['fuel'],
                                    records[i]['packet']['mileage'],
                                    getFormattedDateLocal(records[i]['time'])
                                ];

                   }
                   csvData.push(csvRow);
                   $('#summaryTable').dataTable().fnAddData(row);
                }

                $('#summaryStatus').html('');
                //summaryTable = $('#summaryTable').dataTable({});
            }else{
                var error_msg = '<ul style="color:red">';
                for(var index=0; index < data['error'].length; index++)
                {
                    error_msg += '<li>'+ data['error'][index]  + '</li>';
                }
                error_msg += '<ul>';
                $('#summaryStatus').html(error_msg);
            }
    }).fail(function(jqXHR){
            $('#summaryStatus').html('<font color="red">Unable to load.</font>');//jqXHR.responseText);
    }); 
}



function setErrorlistStyle() {
    $(".errorlist").css({'color': 'red', 'float': 'right'});
}
