/**
 * Event Registration System - Frontend JavaScript
 * Demonstrates browser compatibility issues with datetime-local input
 */

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeForm();
    detectBrowser();
    loadRegistrations();
});

/**
 * Initialize the registration form
 */
function initializeForm() {
    const form = document.getElementById('registrationForm');
    const dateInput = document.getElementById('event_datetime');
    
    // Set minimum date to tomorrow
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const minDate = tomorrow.toISOString().slice(0, 16);
    dateInput.min = minDate;
    
    // Form submission handler
    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        await handleRegistration();
    });
    
    // Track date input changes for debugging
    dateInput.addEventListener('input', function() {
        updateDebugInfo();
    });
}

/**
 * Handle registration form submission
 */
async function handleRegistration() {
    const messageDiv = document.getElementById('message');
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        event_datetime: document.getElementById('event_datetime').value
    };
    
    // Show loading state
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
            loadRegistrations(); // Refresh the list
        } else {
            // BUG DEMONSTRATION: This is where Safari/Firefox users see errors
            showMessage(
                `❌ Registration Failed: ${result.error}\n\n` +
                `This is the browser compatibility bug in action! ` +
                `The backend only accepts ISO 8601 format (YYYY-MM-DDTHH:MM).`,
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

/**
 * Show message to user
 */
function showMessage(text, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = text;
    messageDiv.className = `show ${type}`;
    
    // Auto-hide after 10 seconds for success messages
    if (type === 'success') {
        setTimeout(() => {
            messageDiv.classList.remove('show');
        }, 10000);
    }
}

/**
 * Test different date formats
 */
async function testFormat(dateString) {
    const messageDiv = document.getElementById('message');
    
    // Set the value in the form
    document.getElementById('event_datetime').value = dateString;
    
    // Create test data
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
                `Error: ${result.error}\n\n` +
                `This demonstrates the browser compatibility bug. ` +
                `Safari and Firefox users who manually enter dates in this format ` +
                `cannot complete registration.`,
                'error'
            );
        }
        
        updateDebugInfo(result);
        
    } catch (error) {
        showMessage(`❌ Test failed: ${error.message}`, 'error');
    }
}

/**
 * Load and display current registrations
 */
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

/**
 * Detect browser and update debug info
 */
function detectBrowser() {
    const userAgent = navigator.userAgent;
    let browserName = 'Unknown';
    let browserVersion = 'Unknown';
    let datetimeSupport = 'Unknown';
    
    // Detect browser
    if (userAgent.indexOf('Chrome') > -1 && userAgent.indexOf('Edg') === -1) {
        browserName = 'Chrome';
    } else if (userAgent.indexOf('Edg') > -1) {
        browserName = 'Edge';
    } else if (userAgent.indexOf('Safari') > -1 && userAgent.indexOf('Chrome') === -1) {
        browserName = 'Safari';
    } else if (userAgent.indexOf('Firefox') > -1) {
        browserName = 'Firefox';
    }
    
    // Check datetime-local support
    const input = document.createElement('input');
    input.setAttribute('type', 'datetime-local');
    datetimeSupport = input.type === 'datetime-local' ? 'Yes' : 'No';
    
    // Update debug info
    updateDebugInfo({
        browser: browserName,
        userAgent: userAgent,
        datetimeSupport: datetimeSupport
    });
}

/**
 * Update debug information display
 */
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

/**
 * Utility: Format date for display
 */
function formatDate(dateString) {
    try {
        const date = new Date(dateString);
        return date.toLocaleString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch (e) {
        return dateString;
    }
}
