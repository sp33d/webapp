
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
    makeCustomerTree();
    var sec_30 = 30 * 1000;
    //setInterval(function(){makeCustomerTree();},sec_30);
    //setInterval(function(){refreshFilesSettings();},sec_30);
    initializeToolTip();
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


function removeCustomer(cln, divn) {
    var action_html = '<a class="btn btn-danger" href="javascript:confirmRemovedCustomer(\''+cln+'\', \''+divn+'\')">OK</a>'+
            '<a class="btn btn-primary" data-dismiss="modal" href="javascript:void(0)">Cancel</a>';
    var msg = 'Are you sure you want to remove this customer, and his/her vehicles ?' +
                '<p id="actionStatus"></p>';
    alertBox('Customer deletion alert!', msg, true, action_html);

}

function recycleCustomer(cln, divn) {
    var action_html = '<a class="btn btn-primary" href="javascript:confirmRecycleCustomer(\''+cln+'\', \''+divn+'\')">OK</a>'+
            '<a class="btn " data-dismiss="modal" href="javascript:void(0)">Cancel</a>';
    var msg = 'Are you sure you want to restore this customer, and his/her vehicles ?' +
                '<p id="actionStatus"></p>';
    alertBox('Customer restore alert!', msg, true, action_html);
}

function editCustomerDetails(cln, divn) {
    var action_html = '<a class="btn btn-primary" href="javascript:confirmUpdateCustomer(\''+cln+'\', \''+divn+'\')">Update</a>'+
            '<a class="btn " data-dismiss="modal" href="javascript:void(0)">Cancel</a>';
    var msg = '<p id="actionStatus"></p>';
    alertBox('Edit Customer', msg, true, action_html);
    $('#actionStatus').html('<img src="/static/images/ajax_loader_blue_350.gif" height="10px" width="10px"/>');
    $.ajax({
            url: "/dashboard/ajax/customer-update-form/",
            data: {'ln': cln},
            type: "POST"
    }).done(function(data){
            if( data['status'] == 'success' ) {
                customer_update_form  = data['form']; 
                $('#actionStatus').html(customer_update_form);
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

function showCustomerDetails(cln, divn) {
    var action_html = '<a class="btn btn-primary" data-dismiss="modal" href="javascript:void(0)">OK</a>';
    var msg='<p id="actionStatus"></p>';
    alertBox('Customer Details', msg, true, action_html);
    $('#actionStatus').html('<img src="/static/images/ajax_loader_blue_350.gif" height="10px" width="10px"/>');
    $.ajax({
            url: "/dashboard/ajax/customer-object/",
            data: {'ln': cln},
            type: "POST"
    }).done(function(data){
            if(data['status'] == 'success'){
                var customer_html = '<table>';
                  customer_html += '<tr>';
                    customer_html += '<th>Login Name</th>';
                    customer_html += '<td>' + data['customer']['login_name'] + '</td>';
                  customer_html += '</tr>';
                  customer_html += '<tr>';
                    customer_html += '<th>Password</th>';
                    customer_html += '<td>' + data['customer']['passwd'] + '</td>';
                  customer_html += '</tr>';
                  customer_html += '<tr>';
                    customer_html += '<th>Name</th>';
                    customer_html += '<td>' + data['customer']['name'] + '</td>';
                  customer_html += '</tr>';
                  customer_html += '<tr>';
                    customer_html += '<th>Display Picture</th>';
                    customer_html += '<td>' + data['customer']['display_pic'] + '</td>';
                  customer_html += '</tr>';
                  customer_html += '<tr>';
                    customer_html += '<th>Address</th>';
                    customer_html += '<td>' + data['customer']['address'] + '</td>';
                  customer_html += '</tr>';
                  customer_html += '<tr>';
                    customer_html += '<th>City</th>';
                    customer_html += '<td>' + data['customer']['city'] + '</td>';
                  customer_html += '</tr>';
                  customer_html += '<tr>';
                    customer_html += '<th>Mobile Number</th>';
                    customer_html += '<td>' + data['customer']['mobile_no'] + '</td>';
                  customer_html += '</tr>';
                  customer_html += '<tr>';
                    customer_html += '<th>Email Address</th>';
                    customer_html += '<td>' + data['customer']['email_addr'] + '</td>';
                  customer_html += '</tr>';
                  customer_html += '<tr>';
                    customer_html += '<th>Alert Type</th>';
                    customer_html += '<td>' + data['customer']['alert_type'] + '</td>';
                  customer_html += '</tr>';
                  customer_html += '<tr>';
                    customer_html += '<th>Role</th>';
                    customer_html += '<td>' + data['customer']['role'] + '</td>';
                  customer_html += '</tr>';
                  customer_html += '<tr>';
                    customer_html += '<th>Date of Registration</th>';
                    customer_html += '<td>' + ( new Date(data['customer']['dor']*1000) ) + '</td>';
                  customer_html += '</tr>';
                  customer_html += '<tr>';
                    customer_html += '<th>Valid Till</th>';
                    customer_html += '<td>' + ( new Date(data['customer']['validity_till']*1000) ) + '</td>';
                  customer_html += '</tr>';
                  customer_html += '<tr>';
                    customer_html += '<th>Parent Name</th>';
                    customer_html += '<td>' + data['customer']['parent'] + '</td>';
                  customer_html += '</tr>'; 
                customer_html += '</table>'; 
                $('#actionStatus').html(customer_html);
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



function confirmRemovedCustomer(cln, divn) {
    $('#actionStatus').html('<img src="/static/images/ajax_loader_blue_350.gif" height="10px" width="10px"/>');
    $.ajax({
            url: "/dashboard/ajax/customer-remove/",
            data: {'ln': cln},
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

function confirmRecycleCustomer(cln, divn) {
    $('#actionStatus').html('<img src="/static/images/ajax_loader_blue_350.gif" height="10px" width="10px"/>');
    $.ajax({
            url: "/dashboard/ajax/customer-recycle/",
            data: {'ln': cln},
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
