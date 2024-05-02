
// Verwende wichtige CSS-Stile, um Überschreibungen zu vermeiden
document.body.style.cursor = 'url("logo.jpg"), auto !important';


document.addEventListener('click', function(event) {
  const clickEffect = document.createElement('div');
  clickEffect.style.position = 'absolute';
  clickEffect.style.left = `${event.pageX}px`;
  clickEffect.style.top = `${event.pageY}px`;
  clickEffect.style.width = '20px';
  clickEffect.style.height = '20px';
  clickEffect.style.background = 'red';
  clickEffect.style.borderRadius = '50%';
  clickEffect.style.animation = 'clickAnimation 0.5s forwards';

  document.body.appendChild(clickEffect);

  setTimeout(() => {
    document.body.removeChild(clickEffect);
  }, 500);  // Entfernt den Klick-Effekt nach 0.5 Sekunden
});

// CSS Animation
const style = document.createElement('style');
style.textContent = `
@keyframes clickAnimation {
  from {
    transform: scale(0);
    opacity: 1;
  }
  to {
    transform: scale(1);
    opacity: 0;
  }
}`;
document.head.appendChild(style);
