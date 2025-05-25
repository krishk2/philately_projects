document.addEventListener('DOMContentLoaded', function () {
    // Profile form submission
    document.getElementById('profileForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const email = document.getElementById('email').value;

        // Perform your AJAX or form submission logic here
        console.log('Profile settings updated:', { email });
        alert('Profile updated successfully!');
    });

    // Password form submission
    document.getElementById('passwordForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const currentPassword = document.getElementById('currentPassword').value;
        const newPassword = document.getElementById('newPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        if (newPassword === confirmPassword) {
            // Perform your AJAX or form submission logic here
            console.log('Password updated:', { currentPassword, newPassword });
            alert('Password updated successfully!');
        } else {
            alert('New password and confirm password do not match!');
        }
    });
});
