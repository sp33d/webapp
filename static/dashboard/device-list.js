
$(document).ready(function() {

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    var sec_30 = 30 * 1000;
    //setInterval(function(){makeCustomerTree();},sec_30);
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


function removeDevice(did, divn) {
    var action_html = '<a class="btn btn-danger" href="javascript:confirmRemoveDevice(\''+did+'\', \''+divn+'\')">OK</a>'+
            '<a class="btn btn-primary" data-dismiss="modal" href="javascript:void(0)">Cancel</a>';
    var msg = 'Are you sure you want to remove this  device/vehicle?' +
                '<p id="actionStatus"></p>';
    alertBox('Device deletion alert!', msg, true, action_html);

}

function recycleDevice(did, divn) {
    var action_html = '<a class="btn btn-primary" href="javascript:confirmRecycleDevice(\''+did+'\', \''+divn+'\')">OK</a>'+
            '<a class="btn " data-dismiss="modal" href="javascript:void(0)">Cancel</a>';
    var msg = 'Are you sure you want to restore/recycle this device/vehicle?' +
                '<p id="actionStatus"></p>';
    alertBox('Device restore alert!', msg, true, action_html);
}

function editDeviceDetails(did, divn) {
    var action_html = '<a class="btn btn-primary" href="javascript:confirmUpdateDevice(\''+did+'\', \''+divn+'\')">Update</a>'+
            '<a class="btn " data-dismiss="modal" href="javascript:void(0)">Cancel</a>';
    var msg = '<p id="actionStatus"></p>';
    alertBox('Edit Device', msg, true, action_html);
    $('#actionStatus').html('<img src="/static/images/ajax_loader_blue_350.gif" height="10px" width="10px"/>');
    $.ajax({
            url: "/dashboard/ajax/device-update/",
            data: {'did': did},
            type: "POST"
    }).done(function(data){
            if( data['status'] == 'success' ) {
                var device_update_form = '<form class="form-horizontal" method="post" '+
                    'action="/dashboard/ajax/device-update/" enctype="multipart/form-data"'+
                    'name="device-updation-form" id="device-updation-form">'+
                        '<table width="100%" border="0" cellpadding="0" cellspacing="0">'+
                            data['form'] + 
                        '</table>'+
                    '</form>';
                $('#actionStatus').html(device_update_form);
                setErrorlistStyle();
            }else{
                var error_msg = '<ul style="color:red">';
                for(var index=0; index < data['error'].length; index++)
                {
                    error_msg += '<li>'+ data['error'][index]  + '</li>';
                }
                error_msg += '<ul>';
                $('#actionStatus').html(error_msg);
            }
    }).fail(function(jqXHR){
            $('#actionStatus').html('<font color="red">Unable to load.</font>');//jqXHR.responseText);
    });
}

function showDeviceDetails(did, divn) {
    var action_html = '<a class="btn btn-primary" data-dismiss="modal" href="javascript:void(0)">OK</a>';
    var msg='<p id="actionStatus"></p>';
    alertBox('Device Details', msg, true, action_html);
    $('#actionStatus').html('<img src="/static/images/ajax_loader_blue_350.gif" height="10px" width="10px"/>');
    $.ajax({
            url: "/dashboard/ajax/device-object/",
            data: {'did': did},
            type: "POST"
    }).done(function(data){
            if(data['status'] == 'success'){
                var device_html = '<table>';
                  device_html += '<tr>';
                    device_html += '<th>IMEI</th>';
                    device_html += '<td>' + data['device']['imei'] + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Name</th>';
                    device_html += '<td>' + data['device']['name'] + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Protocol</th>';
                    device_html += '<td>' + data['device']['protocol'] + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Icon</th>';
                    device_html += '<td>' + data['device']['icon'] + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>IMSI</th>';
                    device_html += '<td>' + data['device']['imsi'] + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Stock Status</th>';
                    device_html += '<td>' + data['device']['stock_st'] + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Tank Capacity</th>';
                    device_html += '<td>' + data['device']['tank_sz'] + ' l </td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Fuel Tank Type</th>';
                    device_html += '<td>' + data['device']['fuel_tank'] + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Maximum Speed</th>';
                    device_html += '<td>' + data['device']['max_speed'] + ' KMPH</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Maximum Temprature</th>';
                    device_html += '<td>' + data['device']['max_temp'] + ' C</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Lowest Fuel</th>';
                    device_html += '<td>' + data['device']['lowest_fuel'] + ' l </td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>RC Number</th>';
                    device_html += '<td>' + data['device']['rc_number'] + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>RC Date</th>';
                    device_html += '<td>' + ( new Date(data['device']['rc_date']*1000) ) + ' </td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Insurance Number</th>';
                    device_html += '<td>' + data['device']['insurance_number'] + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Insurance Company</th>';
                    device_html += '<td>' + data['device']['insurance_company'] + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Insurance Date</th>';
                    device_html += '<td>' + (new Date(data['device']['insurance_date']*1000) ) + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Insurance Due Date</th>';
                    device_html += '<td>' + (new Date(data['device']['insurance_due_date']*1000) ) + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Insurance Premium</th>';
                    device_html += '<td>Rs. ' + data['device']['insurance_premium'] + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Servicing Due Date</th>';
                    device_html += '<td>' + (new Date(data['device']['tank_sz']*1000) ) + ' </td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Servicing Due After</th>';
                    device_html += '<td>' + data['device']['servicing_due_km'] + ' KM</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Odometer Reading</th>';
                    device_html += '<td>' + data['device']['odometer_reading'] + ' KM</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Driver Display Picture</th>';
                    device_html += '<td>' + data['device']['driver_dp'] + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Driver Name</th>';
                    device_html += '<td>' + data['device']['driver_name'] + ' L </td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Driver Address</th>';
                    device_html += '<td>' + data['device']['driver_addr'] + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Driver Contact No</th>';
                    device_html += '<td>' + data['device']['driver_contact_no'] + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>License Number</th>';
                    device_html += '<td>' + data['device']['license_no'] + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>License Expiry Date</th>';
                    device_html += '<td>' + (new Date(data['device']['license_exp_date']*1000) ) + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Contract Company</th>';
                    device_html += '<td>' + data['device']['contract_company'] + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Contract Amount</th>';
                    device_html += '<td>Rs. ' + data['device']['contract_amt'] + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Contract Renewal Date</th>';
                    device_html += '<td>' + (new Date(data['device']['contract_renewal_dt']*1000)) + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Contract Date</th>';
                    device_html += '<td>' + (new Date(data['device']['contract_date']*1000)) + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Subscription Amount</th>';
                    device_html += '<td>Rs. ' + data['device']['subscription_amt'] + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Owner</th>';
                    device_html += '<td>' + data['device']['owner'] + '</td>';
                  device_html += '</tr>';
                  device_html += '<tr>';
                    device_html += '<th>Date of Registration</th>';
                    device_html += '<td>' + (new Date(data['device']['dor']*1000) ) + '</td>';
                  device_html += '</tr>';
                device_html += '</table>'; 
                $('#actionStatus').html(device_html);
            }else{
                var error_msg = '<ul style="color:red">';
                for(var index=0; index < data['error'].length; index++)
                {
                    error_msg += '<li>'+ data['error'][index]  + '</li>';
                }
                error_msg += '<ul>';
                $('#actionStatus').html(error_msg);
            }
    }).fail(function(jqXHR){
            $('#actionStatus').html('<font color="red">Unable to load.</font>');//jqXHR.responseText);
    }); 
}



function confirmRemoveDevice(did, divn) {
    $('#actionStatus').html('<img src="/static/images/ajax_loader_blue_350.gif" height="10px" width="10px"/>');
    $.ajax({
            url: "/dashboard/ajax/device-remove/",
            data: {'did': did},
            type: "POST"
    }).done(function(data){
            if(data['status'] == 'success'){
                $('#'+divn).html('Removed!');
                $('#alertModalBox').modal('hide');
            }else{
                var error_msg = '<ul style="color:red">';
                for(var index=0; index < data['error'].length; index++)
                {
                    error_msg += '<li>'+ data['error'][index]  + '</li>';
                }
                error_msg += '<ul>';
                $('#actionStatus').html(error_msg);
            }
    }).fail(function(jqXHR){
            $('#actionStatus').html('<font color="red">Unable to load.</font>');//jqXHR.responseText);
    });
}

function confirmRecycleDevice(did, divn) {
    $('#actionStatus').html('<img src="/static/images/ajax_loader_blue_350.gif" height="10px" width="10px"/>');
    $.ajax({
            url: "/dashboard/ajax/device-recycle/",
            data: {'did': did},
            type: "POST"
    }).done(function(data){
            if(data['status'] == 'success'){
                $('#'+divn).html('Restored!');
                $('#alertModalBox').modal('hide');
            }else{
                var error_msg = '<ul style="color:red">';
                for(var index=0; index < data['error'].length; index++)
                {
                    error_msg += '<li>'+ data['error'][index]  + '</li>';
                }
                error_msg += '<ul>';
                $('#actionStatus').html(error_msg);
            }
    }).fail(function(jqXHR){
            $('#actionStatus').html('<font color="red">Unable to load.</font>');//jqXHR.responseText);
    });
}


function confirmUpdateDevice(did, divn) {
    var frm = $('#device-updation-form');
    frm.submit(function () {
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                if(data['status'] == 'success'){
                    if(data['form_saved']){
                        //Data saved show success msg
                        var msg = '<div class="alert alert-success">'+
                            '<button class="close" data-dismiss="alert">x</button>'+
                            '<strong>Success! </strong>' +
                            'Details updated.'+
                            '</div>';
                        //$("#actionStatus").html(msg);
                        $('#'+divn).html('Updated!');
                        $('#alertModalBox').modal('hide');
                    }else{
                        //Something wrong with the form, show it again
                        var device_update_form = '<form class="form-horizontal" method="post" '+
                            'action="/dashboard/ajax/device-update/" enctype="multipart/form-data"'+
                            'name="device-updation-form" id="device-updation-form">'+
                                '<table width="100%" border="0" cellpadding="0" cellspacing="0">'+
                                    data['form'] +
                                '</table>'+
                            '</form>';
                        $("#actionStatus").html(device_update_form); 
                        setErrorlistStyle();
                    }
                }else{
                    //Some BL error
                    var error_msg = '<ul style="color:red">';
                    for(var index=0; index < data['error'].length; index++)
                    {
                        error_msg += '<li>'+ data['error'][index]  + '</li>';
                    }
                    error_msg += '<ul>';
                    $('#actionStatus').html(error_msg);
                }
            },
            error: function(data) {
                $("#actionStatus").html("<font color='red'>Something went wrong!</font>");
            }
        });
        return false;
    });
    frm.submit();
}

function setErrorlistStyle() {
    $(".errorlist").css({'color': 'red', 'float': 'right'});
}
