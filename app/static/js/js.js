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

    // wiki search API
    document.getElementById('help-content').style.display = 'none';
    document.getElementById('toggle-icon').classList.add('fa-chevron-down');
    document.getElementById('loadContent').addEventListener('click', function() {
        const searchTerm = document.getElementById('searchTerm').value;
        const content = document.getElementById('apiContent');
        if (searchTerm.trim() === "") {
            content.innerHTML = "<p>Please enter a search term.</p>";
            return;
        }
        fetch(`https://en.wikipedia.org/w/api.php?action=query&titles=${searchTerm}&format=json&prop=extracts&origin=*`)
            .then(response => response.json())
            .then(data => {
                const pages = data.query.pages;
                const pageId = Object.keys(pages)[0];
                if (pageId === "-1") {
                    content.innerHTML = "<p>No results found. Try another search term.</p>";
                } else {
                    content.innerHTML = pages[pageId].extract;
                }
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                content.innerHTML = "<p>Error fetching data. Please try again later.</p>";
            });
    });
});

function toggleHelp() {
    var helpContent = document.getElementById('help-content');
    var toggleIcon = document.getElementById('toggle-icon');
    if (helpContent.style.display === 'none' || helpContent.style.display === '') {
        helpContent.style.display = 'block';
        toggleIcon.classList.remove('fa-chevron-down');
        toggleIcon.classList.add('fa-chevron-up');
    } else {
        helpContent.style.display = 'none';
        toggleIcon.classList.remove('fa-chevron-up');
        toggleIcon.classList.add('fa-chevron-down');
    }
}

