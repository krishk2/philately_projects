// Elements for the buttons and tab contents
const philatelistBtn = document.getElementById('philatelist-btn');
const postalCircleBtn = document.getElementById('postalcircle-btn');
const philatelistContent = document.getElementById('philatelists-content');
const postalCircleContent = document.getElementById('postalcircles-content');

// Event listeners for switching tabs
philatelistBtn.addEventListener('click', function() {
  philatelistContent.style.display = 'block';
  postalCircleContent.style.display = 'none';
});

postalCircleBtn.addEventListener('click', function() {
  postalCircleContent.style.display = 'block';
  philatelistContent.style.display = 'none';
});
