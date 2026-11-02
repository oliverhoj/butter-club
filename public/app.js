const form = document.querySelector('#reservation-form');
const button = form.querySelector('button');
const error = document.querySelector('#form-error');
const confirmation = document.querySelector('#confirmation');
// Demo reservation: show the completed flow locally without contacting a server.
form.addEventListener('submit', async event => {
  event.preventDefault();
  if (button.disabled) return;
  error.textContent = '';
  const name = form.elements.name.value.trim();
  if (!name) { error.textContent = 'Kokken har brug for et navn til din stol.'; return; }
  const guests = Number(form.elements.guests.value);
  const time = form.elements.time.value;
  button.disabled = true;
  button.textContent = 'Kokken finder en stol …';
  form.setAttribute('aria-busy', 'true');
  await new Promise(resolve => setTimeout(resolve, 850));
  document.querySelector('#confirmation-text').textContent = `Der er plads til ${guests} ${guests === 1 ? 'person' : 'personer'} kl. ${time}. Kom sulten — vi ses i sofaen!`;
  form.hidden = true;
  confirmation.hidden = false;
  confirmation.focus();
  form.removeAttribute('aria-busy');
  button.disabled = false;
  button.innerHTML = 'Gem en portion til mig <span>↗</span>';
});
document.querySelector('#another').addEventListener('click', () => {
  form.reset(); form.hidden = false; confirmation.hidden = true;
  form.elements.name.focus();
});
