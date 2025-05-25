document.addEventListener('DOMContentLoaded', () => {
    const updateForm = document.getElementById('updateForm');
    const stockForm = document.getElementById('stockForm');

    updateForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const updateType = document.getElementById('updateType').value;
        const updateTitle = document.getElementById('updateTitle').value;
        const updateContent = document.getElementById('updateContent').value;

        // Handle the update (e.g., send to server or save locally)
        console.log('New Update:', { updateType, updateTitle, updateContent });
        alert('Update posted successfully!');
    });

    stockForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const item = document.getElementById('item').value;
        const quantity = document.getElementById('quantity').value;

        // Handle stock update (e.g., send to server or save locally)
        console.log('Stock Update:', { item, quantity });
        alert('Stock updated successfully!');
    });
});
