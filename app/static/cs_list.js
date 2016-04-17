/**
 * Created by colin on 4/15/16.
 */

// Top-level click handler
function clickHandler(e) {
    console.log('clickHandler! ' + e.target.id);
    if (e.target.id.length > 2) {
        var typ = e.target.id.substr(0, 1);
        var csid = e.target.id.substr(2);
        if (typ == 'e' || typ == 'E') {
            // Edit
            var newLocation = '/cs_entry/' + csid;
            window.location = newLocation;
        }
        else if (typ == 'u' || typ == 'U') {
            // Upload display project
            var newLocation = '/upload/' + csid;
            window.location = newLocation;
        }
        else if (typ == 'd' || typ == 'D') {
            // Delete
            var newLocation = '/cs_delete/' + csid;
            window.location = newLocation;
        }
    }
}

window.onload = function() {
    var blist = document.querySelectorAll('button.cresButton');
    for (var i = 0; i < blist.length; i++) {
        var b = blist[i];
        b.addEventListener('click', clickHandler, false);
    }
};

