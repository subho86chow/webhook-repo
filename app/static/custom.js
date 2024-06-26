
async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        return null;
    }
}


function fetchAPIdata(){
    let url = window.location.origin + '/get-data-api';
    fetchData(url)
    .then(data => {
    const defaultScreen = document.getElementById('default_screen');
    defaultScreen.innerHTML = '';


    for (let i = 0; i < data.length; i++) {
        let alertHTML = '';
        
        if (data[i].action_type == 'push') {
            alertHTML = `
                <div class="alert alert-secondary" role="alert">
                    "${data[i].author}" <span class="badge badge-pill badge-success">pushed</span> to "${data[i].to_branch}" on ${formatDate(data[i].timestamp)}
                </div>
            `;
        } else if (data[i].action_type == 'pull_request') {
            alertHTML = `
                <div class="alert alert-secondary" role="alert">
                    "${data[i].author}" submitted a  <span class="badge badge-pill badge-warning">pull</span> request from "${data[i].from_branch}" to "${data[i].to_branch}" on ${formatDate(data[i].timestamp)}
                </div>
            `;
        } else if (data[i].action_type == 'merge') {
            alertHTML = `
                <div class="alert alert-secondary" role="alert">
                    "${data[i].author}" <span class="badge badge-pill badge-info">merged</span> from "${data[i].from_branch}" to "${data[i].to_branch}" on ${formatDate(data[i].timestamp)}
                </div>
            `;
        }

        defaultScreen.innerHTML += alertHTML;
    }

    function formatDate(timestamp) {

        if (timestamp && timestamp.$date) {
            timestamp = timestamp.$date;
        }

        const date = new Date(timestamp);
        if (isNaN(date.getTime())) {
            console.error("Failed to parse timestamp");
            return "Invalid Date";
        }
    
        const day = date.getUTCDate().toString().padStart(2, '0');
        const monthNames = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"];
        const month = monthNames[date.getUTCMonth()];
        const year = date.getUTCFullYear();
        
        let hours = date.getUTCHours();
        const minutes = date.getUTCMinutes().toString().padStart(2, '0');
        const ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12;
        hours = hours.toString().padStart(2, '0');
    
        return `${day} ${month} ${year} - ${hours}:${minutes} ${ampm} UTC`;
    }

    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}




function setupAutoRefresh() {
    const intervalTime = 15000;
    const alertTime = 3000;
    const alertDiv = document.getElementById('autorefresh_alert');
    
    function updateAlertText(seconds) {
        alertDiv.innerHTML = `<i class="bi bi-arrow-clockwise mr-2"></i>Auto Refresh in ${seconds} second${seconds !== 1 ? 's' : ''}.`;
    }

    function showAlert() {
        alertDiv.style.display = 'block';
        let secondsLeft = 3;
        updateAlertText(secondsLeft);

        const countdownInterval = setInterval(() => {
            secondsLeft--;
            if (secondsLeft > 0) {
                updateAlertText(secondsLeft);
            } else {
                clearInterval(countdownInterval);
                alertDiv.style.display = 'none';
            }
        }, 1000);
    }

    function refreshData() {
        console.log('Refreshing data...');
        fetchAPIdata();
    }

    function runCycle() {
        setTimeout(() => {
            showAlert();
            setTimeout(() => {
                refreshData();
                runCycle();
            }, alertTime);
        }, intervalTime - alertTime);
    }
    alertDiv.style.display = 'none';

    runCycle();
}

document.addEventListener('DOMContentLoaded', setupAutoRefresh);