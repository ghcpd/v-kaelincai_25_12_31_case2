/* Frontend JS copied from original project (unchanged) */

document.addEventListener('DOMContentLoaded', function() {
    initializeForm();
    detectBrowser();
    loadRegistrations();
});

function initializeForm() {
    const form = document.getElementById('registrationForm');
    const dateInput = document.getElementById('event_datetime');
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const minDate = tomorrow.toISOString().slice(0, 16);
    dateInput.min = minDate;
    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        await handleRegistration();
    });
    dateInput.addEventListener('input', function() {
        updateDebugInfo();
    });
}

async function handleRegistration() {
    const messageDiv = document.getElementById('message');
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        event_datetime: document.getElementById('event_datetime').value
    };
    showMessage('Submitting registration...', 'info');
    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        const result = await response.json();
        if (result.success) {
            showMessage(
                `✅ Success! ${result.message} on ${result.event_date}`,
                'success'
            );
            document.getElementById('registrationForm').reset();
            loadRegistrations();
        } else {
            showMessage(
                `❌ Registration Failed: ${result.error}`,
                'error'
            );
        }
        updateDebugInfo(result);
    } catch (error) {
        showMessage(
            `❌ Network Error: ${error.message}`,
            'error'
        );
    }
}

function showMessage(text, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = text;
    messageDiv.className = `show ${type}`;
    if (type === 'success') {
        setTimeout(() => {
            messageDiv.classList.remove('show');
        }, 10000);
    }
}

async function testFormat(dateString) {
    const messageDiv = document.getElementById('message');
    document.getElementById('event_datetime').value = dateString;
    const testData = {
        name: 'Test User',
        email: 'test@example.com',
        event_datetime: dateString
    };
    showMessage(`Testing format: "${dateString}"...`, 'info');
    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(testData)
        });
        const result = await response.json();
        if (result.success) {
            showMessage(
                `✅ Format "${dateString}" worked!\n` +
                `Successfully registered for ${result.event_date}`,
                'success'
            );
            loadRegistrations();
        } else {
            showMessage(
                `❌ Format "${dateString}" failed!\n\n` +
                `Error: ${result.error}`,
                'error'
            );
        }
        updateDebugInfo(result);
    } catch (error) {
        showMessage(`❌ Test failed: ${error.message}`, 'error');
    }
}

async function loadRegistrations() {
    const listDiv = document.getElementById('registrationsList');
    try {
        const response = await fetch('/api/registrations');
        const data = await response.json();
        if (data.count === 0) {
            listDiv.innerHTML = '<div class="no-registrations">No registrations yet</div>';
        } else {
            listDiv.innerHTML = data.registrations.map((reg, index) => `
                <div class="registration-item">
                    <strong>${index + 1}. ${reg.name}</strong> (${reg.email})
                    <br>
                    <small>Event: ${reg.event_name} - ${reg.event_datetime}</small>
                </div>
            `).join('');
        }
    } catch (error) {
        listDiv.innerHTML = `<div class="error">Failed to load registrations: ${error.message}</div>`;
    }
}

function detectBrowser() {
    const userAgent = navigator.userAgent;
    let browserName = 'Unknown';
    let datetimeSupport = 'Unknown';
    if (userAgent.indexOf('Chrome') > -1 && userAgent.indexOf('Edg') === -1) {
        browserName = 'Chrome';
    } else if (userAgent.indexOf('Edg') > -1) {
        browserName = 'Edge';
    } else if (userAgent.indexOf('Safari') > -1 && userAgent.indexOf('Chrome') === -1) {
        browserName = 'Safari';
    } else if (userAgent.indexOf('Firefox') > -1) {
        browserName = 'Firefox';
    }
    const input = document.createElement('input');
    input.setAttribute('type', 'datetime-local');
    datetimeSupport = input.type === 'datetime-local' ? 'Yes' : 'No';
    updateDebugInfo({
        browser: browserName,
        userAgent: userAgent,
        datetimeSupport: datetimeSupport
    });
}

function updateDebugInfo(additionalInfo = {}) {
    const debugDiv = document.getElementById('debugInfo');
    const dateInput = document.getElementById('event_datetime');
    const info = {
        'Browser': additionalInfo.browser || navigator.userAgent.split(' ').pop(),
        'datetime-local Support': additionalInfo.datetimeSupport || 'Checking...',
        'Current Input Value': dateInput.value || '(empty)',
        'Input Type': dateInput.type,
        'Value Length': dateInput.value ? dateInput.value.length : 0,
        ...additionalInfo
    };
    debugDiv.innerHTML = Object.entries(info)
        .map(([key, value]) => `<div><strong>${key}:</strong> ${value}</div>`)
        .join('');
}
