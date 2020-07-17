document.addEventListener('DOMContentLoaded', () => {

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // Collect task ids from page
    let imagetasks = document.querySelectorAll('.imagetask')
    let tasksid = []
    for (let i = 0; i < imagetasks.length; i++) {
        tasksid.push(imagetasks[i].innerText);
    }
    // When connected, send task ids to check
    socket.on('connect', () => {
        socket.emit('check status', { 'data': tasksid })
        console.log('Sending IDs to check... ' + tasksid)
    });


    // Receive update to task status
    socket.on('update pending', data => {
        let pending = data['ID'].length
        if (pending != 0) {
            socket.emit('check status', { 'data': tasksid })
            console.log('Checking Pending IDs... ' + data['ID'])
        }
        else {
            console.log('All Done')
        }
        socket.on('update complete', data => {
            let completeid = data['ID']
            for (let i = 0; i < completeid.length; i++) {
                let p = document.getElementById(completeid[i])
                let s = p.nextElementSibling
                s.className = 'SUCCESS'
                s.style.color = '#6c757d'
                s.innerText = 'Status: SUCCESS'
            }
        });
    });

    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })


    const copyStyles = document.getElementById("stylebutton");
    const copyIDs = document.getElementById("pdpbutton");
    const copyCDPs = document.getElementById("cdpbutton");

    const styleEx = document.getElementById("samplestyle");
    const pdpEx = document.getElementById("samplepdp");
    const cdpEx = document.getElementById("samplecdp");

    copyStyles.onclick = () => {
        styleEx.focus()
        styleEx.select()
        document.execCommand("copy");
        alert("Copied! Let's check these style for images!");
        window.location = 'image'
    }
    copyIDs.onclick = () => {
        pdpEx.focus()
        pdpEx.select()
        document.execCommand("copy");
        alert("Copied! Let's check the products details!");
        window.location = 'pdp'
    }
    copyCDPs.onclick = () => {
        cdpEx.focus()
        cdpEx.select()
        document.execCommand("copy");
        alert("Copied! Let's find all IDs on a CDP!");
        window.location = 'cdp'
    }
});

