// document.addEventListener('DOMContentLoaded', () => {
    
//     var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    
//     // Identify which task we're on 
//     const taskType = window.location.pathname.replace('/','')
//     console.log('Task Type: '+ taskType)

//     let tasks = document.querySelectorAll('.PENDINGIds')

//     // Only check if there are pending IDs
//     if (tasks.length != 0) {
//         socket.on('connect', () => {
//             var checkTasks = setInterval(myChecking, 5000)
//             console.log('Socket Connected')
            
//             // Receive update to task status
//             socket.on('update complete', data => {
//                 let completeid = data['ID']
//                 console.log('Updating Complete IDs...' + completeid)
//                 for (let i = 0; i < completeid.length; i++) {
//                     let p = document.getElementById(completeid[i])
//                     p.className = 'SUCCESSIds'
//                     let s = p.nextElementSibling
//                     s.className = 'SUCCESS'
//                     s.style.color = '#6c757d'
//                     s.innerText = 'Status: SUCCESS'
//                 }
//                 alert('New Task Completed!')
//                 let tasks = document.querySelectorAll('.PENDINGIds')
//                 if (tasks.length == 0) {
//                     clearInterval(checkTasks);
//                 }
//             });
//         });
//     }
    
//     function myChecking() {
//         // Collect all pending tasks from page
//         let tasks = document.querySelectorAll('.PENDINGIds')
//         let tasksid = []
//         for (let i = 0; i < tasks.length; i++) {
//             tasksid.push(tasks[i].innerText);
//         }
//         // send task ids to check 
//         socket.emit('check status', { 'ids': tasksid, 'task': taskType })
//         console.log('Sending IDs to check... ' + tasksid)
//     }
// });