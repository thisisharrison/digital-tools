function myChecking() {

    // Find section text from server
    console.log("Checking starts now...")

    const taskType = window.location.pathname.replace('/', '')
    const queue = document.getElementById('queue')
    console.log('Task Type: ' + taskType)

    fetch(`/queue/${taskType}`)
        .then(response => response.text())
        .then(text => {
            // Log text and display on page
            console.log("AJAX udpated");
            queue.innerHTML = text;
        })
}

document.addEventListener('DOMContentLoaded', () => {
    
    // Loads the Queue
    myChecking();

    const refresh = document.querySelector('#refresh')
    refresh.addEventListener("onclick", myChecking);

    
});

