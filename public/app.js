const form = document.querySelector('#reservation-form');
const button = form.querySelector('button');
const error = document.querySelector('#form-error');
const confirmation = document.querySelector('#confirmation');
const pendingKey = 'butter-club-pending';
form.addEventListener('submit', async event => {
  event.preventDefault();
  error.textContent = '';
  const name = form.elements.name.value.trim();
  if (!name) { error.textContent = 'Kokken har brug for et navn til din stol.'; return; }
  const values = {name, guests: Number(form.elements.guests.value), time: form.elements.time.value, note: form.elements.note.value.trim()};
  let id = typeof crypto.randomUUID === 'function' ? crypto.randomUUID() : 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => { const n = crypto.getRandomValues(new Uint8Array(1))[0] & 15; return (c === 'x' ? n : (n & 3) | 8).toString(16); });
  try {
    const previous = JSON.parse(sessionStorage.getItem(pendingKey) || 'null');
    if (previous && JSON.stringify(previous.values) === JSON.stringify(values)) id = previous.id;
    sessionStorage.setItem(pendingKey, JSON.stringify({id, values}));
  } catch (_) { /* Booking still works when browser storage is disabled. */ }
  button.disabled = true;
  button.textContent = 'Kokken finder en stol …';
  try {
    const response = await fetch('/api/reservations', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({...values, id})});
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'Din reservation kunne ikke gemmes.');
    document.querySelector('#confirmation-text').textContent = `${name}, der er gemt plads til ${values.guests} ${values.guests === 1 ? 'person' : 'personer'} kl. ${values.time}. Kom sulten — vi ses ved bordet!`;
    form.hidden = true;
    confirmation.hidden = false;
    confirmation.focus();
    try { sessionStorage.removeItem(pendingKey); } catch (_) {}
  } catch (err) {
    error.textContent = err instanceof TypeError || err instanceof SyntaxError ? 'Vi kunne ikke få fat i køkkenet. Tjek forbindelsen, og prøv igen. Din plads er først gemt, når du ser en bekræftelse.' : err.message;
  } finally {
    button.disabled = false;
    button.innerHTML = 'Gem en portion til mig <span>↗</span>';
  }
});
document.querySelector('#another').addEventListener('click', () => {
  form.reset(); form.hidden = false; confirmation.hidden = true;
  form.elements.name.focus();
});
