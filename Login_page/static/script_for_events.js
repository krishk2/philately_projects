document.addEventListener('DOMContentLoaded', function () {
    // Function to fetch events and populate the dropdown
    function populateEventDropdown() {
        fetch('/get-events')
            .then(response => response.json())
            .then(data => {
                const eventSelect = document.getElementById('existingEvents');
                eventSelect.innerHTML = ''; // Clear existing options

                data.forEach(event => {
                    const option = document.createElement('option');
                    option.value = event.id;
                    option.textContent = event.event_name;
                    eventSelect.appendChild(option);
                });

                // Set the first event's ID in the delete form as a default
                if (data.length > 0) {
                    document.getElementById('deleteEventId').value = data[0].id;
                }
            })
            .catch(error => console.error('Error fetching events:', error));
    }

    // Update hidden delete field when event is selected
    document.getElementById('existingEvents').addEventListener('change', function (e) {
        const selectedEventId = e.target.value;
        document.getElementById('deleteEventId').value = selectedEventId;
    });

    // Call the function to populate the dropdown when the page loads
    populateEventDropdown();
});
