// main.js
const form        = document.getElementById('chat-form'),
      incoming_id = form.querySelector('input[name="incoming_id"]').value,
      inputField  = form.querySelector('.input-field'),
      sendBtn     = form.querySelector('.send-text-btn'),
      recordBtn   = document.getElementById('voice-btn'),
      voiceInput  = document.getElementById('voiceDataInput'),
      meterWrap   = document.getElementById('voiceMeterWrap'),
      meterBar    = document.getElementById('voiceLevel'),
      chatBox     = document.querySelector('.chat-box');

let mediaRecorder,
    audioChunks = [],
    audioContext,
    analyser,
    dataArray,
    rafId;

// Track the one audio instance that’s playing
let currentAudio = null,
    currentBtn   = null;

// Utility: are we currently playing something?
function isAudioPlaying() {
  return currentAudio && !currentAudio.paused;
}

// 1) Bind play/stop toggle on every voice bubble

function bindVoiceControls() {
  document.querySelectorAll('.voice-message').forEach(vm => {
    const audio  = vm.querySelector('.voice-audio');
    const toggle = vm.querySelector('.toggle-play-btn');

    toggle.onclick = () => {
      // stop any other clip first
      if (currentAudio && currentAudio !== audio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
        currentBtn.innerHTML = '<i class="fas fa-play"></i>';
        currentAudio = null;
        currentBtn   = null;
      }

      // toggle this one
      if (audio.paused) {
        audio.play();
        toggle.innerHTML = '<i class="fas fa-stop"></i>';
        currentAudio = audio;
        currentBtn   = toggle;
      } else {
        audio.pause();
        audio.currentTime = 0;
        toggle.innerHTML = '<i class="fas fa-play"></i>';
        currentAudio = null;
        currentBtn   = null;
      }
    };

    audio.onended = () => {
      toggle.innerHTML = '<i class="fas fa-play"></i>';
      if (currentAudio === audio) {
        currentAudio = null;
        currentBtn   = null;
      }
    };
  });
}

// 2) Intercept text form submit
form.addEventListener('submit', e => {
  e.preventDefault();
  sendMessage();
});

// 3) Enable send-text only if there's text
inputField.addEventListener('input', () => {
  sendBtn.disabled = !inputField.value.trim();
});
sendBtn.disabled = true;

// 4) Recording toggle + immediate send
recordBtn.addEventListener('click', async () => {
  if (!mediaRecorder || mediaRecorder.state === 'inactive') {
    // Hide text UI
    inputField.style.display = 'none';
    sendBtn.style.display    = 'none';
    meterWrap.style.display  = 'inline-block';

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    // Meter setup
    audioContext = new AudioContext();
    const src = audioContext.createMediaStreamSource(stream);
    analyser = audioContext.createAnalyser();
    src.connect(analyser);
    analyser.fftSize = 256;
    dataArray = new Uint8Array(analyser.frequencyBinCount);

    (function draw() {
      analyser.getByteFrequencyData(dataArray);
      const avg = dataArray.reduce((a,b)=>a+b,0) / dataArray.length;
      meterBar.style.width = Math.min(100, (avg/128)*100) + '%';
      rafId = requestAnimationFrame(draw);
    })();

    mediaRecorder.ondataavailable = e => {
      if (e.data.size) audioChunks.push(e.data);
    };

    mediaRecorder.onstop = () => {
      cancelAnimationFrame(rafId);
      meterBar.style.width = '0%';

      // Wrap in File for FormData
      const blob = new Blob(audioChunks, { type: 'audio/webm' });
      const file = new File([blob], `voice_${Date.now()}.webm`, { type: blob.type });
      const dt   = new DataTransfer();
      dt.items.add(file);
      voiceInput.files = dt.files;

      // Restore text UI
      inputField.style.display = '';
      sendBtn.style.display    = '';
      meterWrap.style.display  = 'none';

      // Send it
      sendMessage();

      // Reset
      mediaRecorder = null;
      audioChunks   = [];
      recordBtn.innerHTML = '<i class="fas fa-microphone"></i>';
    };

    mediaRecorder.start();
    recordBtn.innerHTML = '<i class="fas fa-stop"></i>';
  } else {
    mediaRecorder.stop();  // triggers onstop
  }
});

// 5) AJAX send
function sendMessage() {
  const xhr = new XMLHttpRequest();
  xhr.open('POST', 'php/insert-chat.php', true);
  xhr.onload = () => {
    if (xhr.status === 200) {
      inputField.value = '';
      voiceInput.value = '';
      scrollToBottom();
    }
  };
  xhr.send(new FormData(form));
}

// 6) Poll for new messages—but pause polling if playback is active
setInterval(() => {
  if (isAudioPlaying()) return;

  const xhr = new XMLHttpRequest();
  xhr.open('POST', 'php/get-chat.php', true);
  xhr.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
  xhr.onload = () => {
    if (xhr.readyState === 4 && xhr.status === 200) {
      chatBox.innerHTML = xhr.responseText;
      bindVoiceControls();
      if (!chatBox.classList.contains('active')) {
        scrollToBottom();
      }
    }
  };
  xhr.send('incoming_id=' + encodeURIComponent(incoming_id));
}, 500);

// 7) Pause auto-scroll when hovering
chatBox.addEventListener('mouseenter', () => chatBox.classList.add('active'));
chatBox.addEventListener('mouseleave', () => chatBox.classList.remove('active'));

// 8) Scroll helper
function scrollToBottom() {
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Initial bind in case there’s pre-existing messages
bindVoiceControls();
