document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.notification-read, .notification-link').forEach(element => {
        element.addEventListener('click', function (event) {
            if (this.classList.contains('notification-read')) {
                event.preventDefault();
            }

            const csrftoken = document.querySelector('#notification_wrapper').getAttribute('data-csrf-token');
            const parentElement = this.closest('.notification-item');
            const notificationId = parentElement.getAttribute('data-notification-id');
            const actionUrl = parentElement.getAttribute('data-notification-action-url');

            mark_as_read(csrftoken, notificationId, actionUrl);
        });
    });
});

function mark_as_read(csrftoken, notificationId, actionUrl) {
    fetch(actionUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ notificationId }),
    })
    .then(response => {
        document.getElementById(`notification_${notificationId}`).remove();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
