document.addEventListener('DOMContentLoaded', () => {

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