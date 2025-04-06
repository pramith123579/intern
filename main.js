async function checkBackendConnection() {
    try {
        const response = await fetch('http://127.0.0.1:5000/'); // Ensure this matches the backend URL
        if (!response.ok) {
            throw new Error('Backend is not reachable');
        }
        console.log('Backend is running!');
    } catch (error) {
        console.error('Error connecting to backend:', error);
        alert('Unable to connect to the backend. Please ensure the server is running.');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    checkBackendConnection(); // Check backend connection on page load

    const loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));

    if (loggedInUser) {
        document.getElementById('user-name').textContent = loggedInUser.username;
    } else {
        window.location.href = 'index.html';
    }

    document.getElementById('health-data-form').addEventListener('submit', async function (e) {
        e.preventDefault();

        const healthData = {
            name: document.getElementById('user-name-input').value,
            bp: document.getElementById('blood-pressure').value,
            sugar: document.getElementById('blood-sugar').value,
            temp: document.getElementById('body-temperature').value,
            symptom: document.getElementById('symptom').value
        };

        try {
            const response = await fetch('http://127.0.0.1:5000/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(healthData),
            });

            if (!response.ok) {
                throw new Error('Failed to fetch health advice. Please check the backend server.');
            }

            const result = await response.json();

            const adviceContent = document.getElementById('advice-content');
            adviceContent.innerHTML = `
                <h3>Health Analysis</h3>
                <p><strong>Blood Pressure:</strong> ${result['Blood Pressure'].message}</p>
                <p><strong>Lifestyle Changes:</strong></p>
                <ul>${result['Blood Pressure'].lifestyle.map(item => `<li>${item}</li>`).join('') || '<li>None</li>'}</ul>
                <p><strong>Medications:</strong></p>
                <ul>${result['Blood Pressure'].medications.map(item => `<li>${item}</li>`).join('') || '<li>None</li>'}</ul>
                <p><strong>Blood Sugar:</strong> ${result['Blood Sugar'].message}</p>
                <p><strong>Lifestyle Changes:</strong></p>
                <ul>${result['Blood Sugar'].lifestyle.map(item => `<li>${item}</li>`).join('') || '<li>None</li>'}</ul>
                <p><strong>Medications:</strong></p>
                <ul>${result['Blood Sugar'].medications.map(item => `<li>${item}</li>`).join('') || '<li>None</li>'}</ul>
                <p><strong>Body Temperature:</strong> ${result['Body Temperature'].message}</p>
                <p><strong>Lifestyle Changes:</strong></p>
                <ul>${result['Body Temperature'].lifestyle.map(item => `<li>${item}</li>`).join('') || '<li>None</li>'}</ul>
                <p><strong>Medications:</strong></p>
                <ul>${result['Body Temperature'].medications.map(item => `<li>${item}</li>`).join('') || '<li>None</li>'}</ul>
                ${result['Body Temperature'].types ? `
                    <p><strong>Types of Fever:</strong></p>
                    <ul>
                        ${result['Body Temperature'].types.map(type => `
                            <li>
                                <strong>${type.type}:</strong> ${type.description}
                                <ul>
                                    <li><strong>Common Symptoms:</strong> ${type.common_symptoms.join(', ')}</li>
                                </ul>
                            </li>
                        `).join('')}
                    </ul>
                ` : ''}
                <p><strong>Symptom Analysis:</strong></p>
                <ul>${result['Symptom Analysis'].medications.map(item => `<li>${item}</li>`).join('') || '<li>None</li>'}</ul>
            `;
        } catch (error) {
            console.error('Error:', error);
            alert(error.message || 'An unexpected error occurred. Please try again.');
        }
    });
});