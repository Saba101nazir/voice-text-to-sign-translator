document.addEventListener('DOMContentLoaded', function () {
    const startBtn = document.getElementById('startBtn');
    const doneBtn = document.getElementById('doneBtn');
    const output = document.getElementById('output');
    const error = document.querySelector('.error-para');

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    recognition.onstart = function () {
        console.log('Voice recognition started. Try speaking into the microphone.');
        startBtn.innerHTML = '<i class="uil uil-microphone"></i> Listening...';
    };

    recognition.onresult = function (event) {
        const current = event.resultIndex;
        const transcript = event.results[current][0].transcript;
        console.log('Voice input: ', transcript);
        displaySignOutput(transcript);
        doneBtn.style.display = 'inline-block';
    };

    recognition.onspeechend = function () {
        recognition.stop();
        startBtn.innerHTML = '<i class="uil uil-microphone"></i> Start Voice Input';
    };

    recognition.onerror = function (event) {
        console.error('Speech recognition error', event.error);
        error.textContent = 'Error occurred in recognition: ' + event.error;
        startBtn.innerHTML = '<i class="uil uil-microphone"></i> Start Voice Input';
    };

    startBtn.addEventListener('click', function () {
        recognition.start();
        doneBtn.style.display = 'none'; // Hide done button when starting recognition
    });

    doneBtn.addEventListener('click', function () {
        // Process the confirmed input (e.g., send to server, display result)
        alert('Processing confirmed input');
        doneBtn.style.display = 'none'; // Hide done button after processing
    });

    function displaySignOutput(text) {
        output.innerHTML = "";
        const words = text.split(' ');
        words.forEach(word => {
            const signElement = document.createElement('div');
            signElement.textContent = word;
            signElement.className = 'sign-word';
            output.appendChild(signElement);
        });
    }
});

function toggleMenu() {
    var navMenu = document.querySelector(".nav_menu");
    var openBtn = document.getElementById("open-menu-btn");
    var closeBtn = document.getElementById("close-menu-btn");

    if (!navMenu.classList.contains("show")) {
        navMenu.classList.add("show");
        openBtn.style.display = "none";
        closeBtn.style.display = "inline-block";
    } else {
        navMenu.classList.remove("show");
        openBtn.style.display = "inline-block";
        closeBtn.style.display = "none";
    }
}
