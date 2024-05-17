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

document.addEventListener('DOMContentLoaded', function() {
    function toggleOpen() {
        document.querySelector('body').classList.toggle('open');
        for (var i = 0; i < links.length; i++) {
            if (document.querySelector('body').classList.contains('open')) {
                links[i].style.transitionDelay = i * 0.25 + 's';
            } else {
                links[i].style.transitionDelay = '0s';
            }
        }
    }

    document.querySelector('#burger').addEventListener('click', toggleOpen);
    var links = document.querySelectorAll('header nav a');
    for (var i = 0; i < links.length; i++) {
        links[i].addEventListener('click', toggleOpen);
    }
});