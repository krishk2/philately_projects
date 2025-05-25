document.addEventListener('DOMContentLoaded', () => {
    const profileForm = document.getElementById('profileForm');
    const profilePicInput = document.getElementById('profilePicInput');
    const profilePic = document.getElementById('profilePic');

    // Load existing profile data
    loadProfileData();

    // Handle profile picture change
    profilePicInput.addEventListener('change', () => {
        const file = profilePicInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = () => {
                profilePic.src = reader.result;
                // Save the profile picture data in localStorage
                localStorage.setItem('profilePic', reader.result);
            };
            reader.readAsDataURL(file);
        }
    });

    // Handle form submission
    profileForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const formData = new FormData(profileForm);
        const profileData = Object.fromEntries(formData.entries());

        // Save profile data in localStorage
        localStorage.setItem('profileData', JSON.stringify(profileData));

        // Simulate saving changes and updating dashboard
        alert('Profile updated successfully!');
        updateDashboard();
    });

    function loadProfileData() {
        const storedProfileData = localStorage.getItem('profileData');
        const storedProfilePic = localStorage.getItem('profilePic');
        
        if (storedProfileData) {
            const profileData = JSON.parse(storedProfileData);
            document.getElementById('name').value = profileData.name || '';
            document.getElementById('email').value = profileData.email || '';
            document.getElementById('membership').value = profileData.membership || 'Basic';
            document.getElementById('aadhaar').value = profileData.aadhaar || '';
        }
        
        if (storedProfilePic) {
            profilePic.src = storedProfilePic;
        }
    }

    function updateDashboard() {
        if (window.opener && window.opener.updateDashboard) {
            window.opener.updateDashboard();
        }
    }
});
document.addEventListener('DOMContentLoaded', () => {
    const profilePicInput = document.getElementById('profilePicInput');
    const profilePic = document.getElementById('profilePic');

    profilePicInput.addEventListener('change', function(event) {
        const file = event.target.files[0];

        if (file) {
            const reader = new FileReader();

            reader.onload = function(e) {
                profilePic.src = e.target.result; // Update the image source
                // Optionally, save the image data in localStorage if needed
                localStorage.setItem('profilePic', e.target.result);
            };

            reader.readAsDataURL(file); // Read the file as a data URL
        }
    });
});

