document.getElementById('registration-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const event_datetime = document.getElementById('event_datetime').value;

  const resp = await fetch('/api/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, event_datetime })
  });

  const result = await resp.json();
  document.getElementById('result').innerText = JSON.stringify(result);
});
