function dismissAlert(element) {
    var alertElement = element.closest('.custom-alert');
    if (alertElement) {
        alertElement.style.display = 'none'; // This hides the alert
    }
}