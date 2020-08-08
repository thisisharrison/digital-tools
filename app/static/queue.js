

document.addEventListener('DOMContentLoaded', () => {

    // Identify which task we're on 
    const taskType = window.location.pathname.replace('/', '')
    const queue = document.getElementById('queue')

    console.log('Task Type: ' + taskType)

    console.log("Checking starts now...")
    var checkTasks = setInterval(myChecking, 3000)
    
    // let tasks = document.querySelectorAll('.PENDINGIds')

    // // Only check if there are pending IDs
    // if (tasks.length == 0) {
    //     var checkTasks = null
    // }
    // if (tasks.length != 0) {
    //     var checkTasks = setInterval(myChecking, 5000)
    // }

    function myChecking() {

        // Find section text from server
        fetch(`/queue/${taskType}`)
            .then(response => response.text())
            .then(text => {
                // Log text and display on page
                console.log("AJAX udpated");
                queue.innerHTML = text;
            });
        
        // console.log("AJAX udpated")
        
        // let tasks = document.querySelectorAll('.PENDINGIds')
        // if (tasks.length == 0) {
        //     clearInterval(checkTasks);
        //     console.log("Interval Cleared!")
        // }
    }
});