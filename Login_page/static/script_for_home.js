document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.querySelector('.carousel');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    let currentIndex = 0;

    function moveCarousel() {
        carousel.style.transform = `translateX(-${currentIndex * 320}px)`;
    }

    nextBtn.addEventListener('click', () => {
        if (currentIndex < carousel.children.length - 1) {
            currentIndex++;
        } else {
            currentIndex = 0;
        }
        moveCarousel();
    });

    prevBtn.addEventListener('click', () => {
        if (currentIndex > 0) {
            currentIndex--;
        } else {
            currentIndex = carousel.children.length - 1;
        }
        moveCarousel();
    });

    setInterval(() => {
        nextBtn.click();
    }, 3000); // Autoplay every 3 seconds
});
document.getElementById('chatbotIcon').addEventListener('click', function() {
    // Show the chatbot interface
    document.getElementById('chatbotInterface').style.display = 'flex';
});

document.getElementById('closeChatbot').addEventListener('click', function() {
    // Hide the chatbot interface
    document.getElementById('chatbotInterface').style.display = 'none';
});

document.getElementById('send-button').addEventListener('click', function() {
    let userInput = document.getElementById('user-input').value;

    if (userInput.trim() === '') return;

    // Display the user's message in the chat log
    let chatLog = document.getElementById('chat-log');
    let userMessage = document.createElement('p');
    userMessage.innerHTML = `<strong>You:</strong> ${userInput}`;
    chatLog.appendChild(userMessage);

    // Clear the input field
    document.getElementById('user-input').value = '';

    // Send the user's input to the Flask backend
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        // Display the bot's response in the chat log
        let botMessage = document.createElement('p');
        botMessage.innerHTML = `<strong>Bot:</strong> ${data.response}`;
        chatLog.appendChild(botMessage);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

            
            
         

