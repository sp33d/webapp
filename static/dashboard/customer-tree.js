var setting = {
    check: {
            enable: true,
            chkboxType: { "Y": "s", "N": "p" } /* If parent is check, auto check child; if child is unchecked auto check parent*/
    },
    data: {
            simpleData: {
                    enable: true
            }
    }
};

var tree = false;

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

function initializeToolTip() {
    $('.tooltip').tooltip();    
    $('.tooltip-left').tooltip({ placement: 'left' });  
    $('.tooltip-right').tooltip({ placement: 'right' });    
    $('.tooltip-top').tooltip({ placement: 'top' });    
    $('.tooltip-bottom').tooltip({ placement: 'bottom' });

    $('.popover-left').popover({placement: 'left', trigger: 'hover'});
    $('.popover-right').popover({placement: 'right', trigger: 'hover'});
    $('.popover-top').popover({placement: 'top', trigger: 'hover'});
    $('.popover-bottom').popover({placement: 'bottom', trigger: 'hover'});

}

function alertBox(title, msg){
    $('#alertModalBoxTitle').html(title);
    $('#alertModalBoxBody').html('<p>' + msg + '</p>');
    $('#alertModalBoxFooter').modal();
}

function makeCustomerTree() {
    $.ajax({
            url: "/dashboard/ajax/customer-tree-json/",
            data: {},
            type: "POST"
    }).done(function(data){
                $('#tree_loader').html('');
                tree = $.fn.zTree.init($("#customerTree"), setting, data);
                tree = $.fn.zTree.getZTreeObj("customerTree");
    }).fail(function(jqXHR){
            $('#tree_loader').html('<font color="red">Unable to load.</font>');//jqXHR.responseText);
    });
}

$('#get_checked_node_btn').click(function(){
    if( tree ) {
        var nodes = tree.getCheckedNodes();
        if( !nodes.length ) {
            alertBox('Alert','Please check atleast one item.');
        }
    }else{
        alertBox('Alert','Wait while the tree is being loaded.');
    }
});

$('#expand_tree').click(function(){
    if( tree ) {
        tree.expandAll(true);
    }else{
        alertBox('Alert','Wait while the tree is being loaded.');
    }
});

$('#shrink_tree').click(function(){
    if( tree ) {
        tree.expandAll(false);
    }else{
        alertBox('Alert','Wait while the tree is being loaded.');
    }
});

$('#uncheck_tree').click(function(){
    if( tree ) {
        tree.checkAllNodes(false);
    }else{
        alertBox('Alert','Wait while the tree is being loaded.');
    }
});

$('#check_all_tree').click(function(){
    if( tree ) {
        tree.checkAllNodes(true);
    }else{
        alertBox('Alert','Wait while the tree is being loaded.');
    }
});

$('#track_selected').click(function(){
    if( tree ) {
        var nodes = tree.getSelectedNodes();
        if( !nodes.length ) {
            alertBox('Alert','Please select a vehicle.');
        }else{
            if( nodes[0].itemType == 'ldevice') {
                //Start tracking the nodes[0].id
            }else{
                alertBox('Alert','Selected item must be a device/vehicle.');
            }
        }
    }else{
        alertBox('Alert','Wait while the tree is being loaded.');
    }
});


$('#clear_selected_item').click(function(){
    if( tree ) {
        tree.selectNode(true);
    }else{
        alertBox('Alert','Wait while the tree is being loaded.');
    }
});
