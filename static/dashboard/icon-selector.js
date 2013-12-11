
function get_ig_icon(state){
    switch(state){
        case true:
            return '<img title="Ignition/ACC On" src="/static/images/icons/acc_on.gif" height="15px" width="15px"/>';
        case false:
            return '<img title="Ignition/ACC Off" src="/static/images/icons/acc_off.gif" height="15px" width="15px"/>';
        default:
            return 'unknown';
    }
}

function get_power_icon(state){
    switch(state){
        case true:
            return '<img title="Main Power Off" src="/static/images/icons/power_off.gif" height="20px" width="20px"/>';
        case false:
            return '<img title="Main Power On" src="/static/images/icons/power_on.gif" height="20px" width="20px"/>';
        default:
            return 'unknown';
    }
}

function get_gps_icon(state){
    switch(state){
        case 'A':
            return '<img title="GPS Signal is Good" src="/static/images/icons/gps_on.gif" height="20px" width="20px"/>';
        case 'V':
            return '<img title="No GPS Signal" src="/static/images/icons/gps_off.gif" height="20px" width="20px"/>';
        default:
            return 'unknown';
    }
}
