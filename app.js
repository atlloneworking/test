const state = {
  selectedSound: localStorage.getItem('selectedSound') || 'chime',
  audioCtx: null,
};

const soundMap = {
  chime: [880, 1320, 1760],
  bell: [660, 990, 1320],
  beep: [900, 900, 900],
  soft: [440, 550, 660],
};

const statusEl = document.getElementById('status');
const soundEl = document.getElementById('sound');
const titleEl = document.getElementById('title');
const messageEl = document.getElementById('message');
const delayEl = document.getElementById('delay');
const previewBtn = document.getElementById('previewSound');
const permissionBtn = document.getElementById('requestPermission');
const scheduleBtn = document.getElementById('scheduleNotification');

soundEl.value = state.selectedSound;

function setStatus(text) {
  statusEl.textContent = text;
}

function getAudioContext() {
  if (!state.audioCtx) {
    state.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
  return state.audioCtx;
}

async function playSound(soundName) {
  const context = getAudioContext();
  const now = context.currentTime;
  const tones = soundMap[soundName] || soundMap.chime;

  tones.forEach((frequency, index) => {
    const oscillator = context.createOscillator();
    const gain = context.createGain();

    oscillator.type = 'sine';
    oscillator.frequency.value = frequency;

    const start = now + index * 0.14;
    gain.gain.setValueAtTime(0.0001, start);
    gain.gain.exponentialRampToValueAtTime(0.2, start + 0.03);
    gain.gain.exponentialRampToValueAtTime(0.0001, start + 0.12);

    oscillator.connect(gain).connect(context.destination);
    oscillator.start(start);
    oscillator.stop(start + 0.13);
  });
}

async function requestNotificationPermission() {
  if (!('Notification' in window)) {
    setStatus('This browser does not support notifications.');
    return false;
  }

  const permission = await Notification.requestPermission();
  setStatus(`Notification permission: ${permission}`);
  return permission === 'granted';
}

async function showNotification(title, body, soundName) {
  const ok = Notification.permission === 'granted' || (await requestNotificationPermission());

  if (!ok) {
    setStatus('Cannot notify without permission.');
    return;
  }

  new Notification(title, { body });
  await playSound(soundName);
  setStatus(`Notification fired with '${soundName}' sound.`);
}

previewBtn.addEventListener('click', async () => {
  const soundName = soundEl.value;
  localStorage.setItem('selectedSound', soundName);
  await playSound(soundName);
  setStatus(`Previewed '${soundName}' sound.`);
});

permissionBtn.addEventListener('click', requestNotificationPermission);

scheduleBtn.addEventListener('click', () => {
  const title = titleEl.value.trim() || 'Reminder';
  const message = messageEl.value.trim() || 'Reminder notification';
  const delay = Number.parseInt(delayEl.value, 10);
  const soundName = soundEl.value;

  if (!Number.isFinite(delay) || delay < 1) {
    setStatus('Delay must be at least 1 second.');
    return;
  }

  localStorage.setItem('selectedSound', soundName);
  setStatus(`Scheduled in ${delay} second(s)...`);

  window.setTimeout(() => {
    showNotification(title, message, soundName);
  }, delay * 1000);
});

if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('sw.js').catch(() => {
    setStatus('Service worker registration failed.');
  });
}
