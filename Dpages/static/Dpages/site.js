const themeButton = document.querySelector('#theme-toggle');
const systemTheme = matchMedia('(prefers-color-scheme: dark)');

function readTheme() {
    try { return localStorage.getItem('draxo-theme'); }
    catch { return null; }
}
function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    themeButton.setAttribute('aria-pressed', String(theme === 'light'));
    themeButton.textContent = theme === 'light' ? 'حالت شب' : 'حالت روز';
}
const systemChoice = () => systemTheme.matches ? 'dark' : 'light';
applyTheme(readTheme() || systemChoice());
systemTheme.addEventListener('change', () => {
    if (!readTheme()) applyTheme(systemChoice());
});
themeButton.addEventListener('click', () => {
    const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('draxo-theme', theme); } catch {}
    applyTheme(theme);
});

const musicButton = document.querySelector('#music-toggle');
const tracks = {
    pubg: [0.30, 'triangle', [43, 50, 55, 58, 41, 48, 53, 55]],
    cod: [0.22, 'triangle', [38, 45, 50, 53, 36, 43, 48, 51]],
    fire: [0.17, 'sine', [50, 57, 62, 65, 48, 55, 60, 67]],
    clash: [0.32, 'sine', [48, 55, 60, 64, 53, 57, 65, 69]],
};

const homeAudio = document.querySelector('#home-soundtrack');
if (musicButton && homeAudio) {
    homeAudio.volume = 0.35;
    const updateMusicState = () => {
        musicButton.setAttribute('aria-pressed', String(!homeAudio.paused));
    };
    homeAudio.addEventListener('play', updateMusicState);
    homeAudio.addEventListener('pause', updateMusicState);
    musicButton.addEventListener('click', async () => {
        if (!homeAudio.paused) {
            homeAudio.pause();
            return;
        }
        musicButton.disabled = true;
        try {
            await homeAudio.play();
            musicButton.removeAttribute('title');
        } catch {
            musicButton.title = "پخش موسیقی در دسترس نیست";
            updateMusicState();
        } finally {
            musicButton.disabled = false;
        }
    });
    window.addEventListener('pagehide', () => homeAudio.pause());
} else if (musicButton && tracks[musicButton.dataset.track]) {
    const [beat, waveform, notes] = tracks[musicButton.dataset.track];
    let context;
    let playing = false;
    let timer;
    let output;

    function playLoop() {
        const start = context.currentTime + 0.03;
        notes.forEach((note, index) => {
            const at = start + index * beat;
            const oscillator = context.createOscillator();
            const envelope = context.createGain();
            oscillator.type = waveform;
            oscillator.frequency.value = 440 * 2 ** ((note - 69) / 12);
            envelope.gain.setValueAtTime(0, at);
            envelope.gain.linearRampToValueAtTime(0.11, at + 0.035);
            envelope.gain.linearRampToValueAtTime(0, at + beat * 1.25);
            oscillator.connect(envelope).connect(output);
            oscillator.start(at);
            oscillator.stop(at + beat * 1.3);
        });
        timer = setTimeout(playLoop, beat * notes.length * 1000);
    }

    function stopMusic() {
        clearTimeout(timer);
        if (output) output.disconnect();
        output = null;
        playing = false;
        musicButton.setAttribute('aria-pressed', 'false');
    }

    musicButton.addEventListener('click', async () => {
        if (playing) {
            stopMusic();
            return;
        }
        musicButton.disabled = true;
        try {
            context ??= new AudioContext();
            await context.resume();
            output = context.createGain();
            output.gain.value = 0.35;
            output.connect(context.destination);
            playing = true;
            playLoop();
            musicButton.setAttribute('aria-pressed', 'true');
        } catch {
            stopMusic();
        } finally {
            musicButton.disabled = false;
        }
    });
    window.addEventListener('pagehide', stopMusic);
}
