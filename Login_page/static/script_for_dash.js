// dashboard.js
window.updateDashboard = function() {
    const profileData = JSON.parse(localStorage.getItem('profileData'));
    const profilePic = localStorage.getItem('profilePic');
    
    if (profileData) {
        document.getElementById('dashboardName').textContent = profileData.name || 'Guest';
        document.getElementById('dashboardEmail').textContent = profileData.email || 'Not provided';
        document.getElementById('dashboardMembership').textContent = profileData.membership || 'Basic';
    }
    
    if (profilePic) {
        document.getElementById('dashboardProfilePic').src = profilePic;
    }
};

// Call this function on page load to set initial values
document.addEventListener('DOMContentLoaded', () => {
    window.updateDashboard();
});
// In the dashboard page script
document.getElementById('editProfileButton').addEventListener('click', () => {
    window.open('profile.html', '_blank');
});
