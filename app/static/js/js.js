function dismissAlert(element) {
    var alertElement = element.closest('.custom-alert');
    if (alertElement) {
        alertElement.style.display = 'none'; // This hides the alert
    }
}

function switchTab(tabId) {
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });

    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });

    document.querySelector(`[onclick="switchTab('${tabId}')"]`).classList.add('active');

    document.getElementById(tabId).classList.add('active');
}