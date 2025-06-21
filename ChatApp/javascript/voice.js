
(() => {
  let mediaRecorder, audioChunks = [];
  const voiceBtn = document.getElementById('voice-btn');
  const form    = document.getElementById('chat-form');

  // 1) request mic access once at load
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.addEventListener('dataavailable', e => {
        audioChunks.push(e.data);
      });

      mediaRecorder.addEventListener('stop', () => {
        const blob = new Blob(audioChunks, { type: 'audio/webm' });
        audioChunks = [];

        // build FormData
        const fd = new FormData();
        fd.append('incoming_id', document.querySelector('.incoming_id').value);
        fd.append('voice_data', blob, `voice_${Date.now()}.webm`);

        // upload
        fetch('php/send_voice.php', {
          method: 'POST',
          body: fd
        })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            // optionally append the new voice message to chat...
            console.log('Voice sent');
          } else {
            alert('Upload failed.');
          }
        })
        .catch(console.error);
      });
    })
    .catch(err => {
      console.error('Mic access denied', err);
      voiceBtn.disabled = true;
    });

  // 2) toggle recording on click
  voiceBtn.addEventListener('click', () => {
    if (!mediaRecorder) return;
    if (mediaRecorder.state === 'inactive') {
      mediaRecorder.start();
      voiceBtn.classList.add('recording');
    } else {
      mediaRecorder.stop();
      voiceBtn.classList.remove('recording');
    }
  });

  // 3) keep your existing text-send handler
  form.addEventListener('submit', e => {
    e.preventDefault();
    // your AJAX/text-send logic here...
  });
})();

