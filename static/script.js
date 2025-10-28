// Function to check if the user is in the list and the password is correct
async function validateUser(licenseNumber, password) {
    try {
        const response = await fetch(`/api/user-by-license/${licenseNumber}`);
        const user = await response.json();
        
        // If user exists and the password matches, return true
        if (user && user.password === password) {
            return true;
        }
        
        // Otherwise, return false
        return false;
    } catch (error) {
        console.error('Error validating user:', error);
        return false;
    }
}

// Function to handle the form submission
async function handleLogin(event) {
    event.preventDefault(); // Prevent form submission

    const licenseNumber = document.getElementById('licenseNumber').value;
    const password = document.getElementById('password').value;

    // Check if the user is valid
    if (await validateUser(licenseNumber, password)) {
        // If valid, redirect to the next page
        window.location.href = "/fingerprint";
    } else {
        // If invalid, show an error message
        alert("Error: The user does not exist or the password is incorrect.");
    }
}

// Function to clear form fields on page load
function clearForm() {
    document.getElementById('licenseNumber').value = '';
    document.getElementById('password').value = '';
}

// Add event listener to the login form
document.getElementById('loginForm').addEventListener('submit', handleLogin);

// Clear form fields when page loads
window.onload = clearForm;