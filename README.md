# Smart Parking Automation Script

## Description
A Python automation script using Selenium to log in to SMRTPass, enter payment info, and purchase daily parking.

## Lessons Learned
I built an automation script using Python and Selenium to automatically purchase my daily parking from the SMRTPass website. The script logs in using saved credentials, enters my CVV, and either clicks the purchase button or submits the form directly as a fallback.

I used WebDriverWait with expected conditions to ensure all elements were loaded before interacting with them, which helped avoid timing issues. I stored sensitive information like email, password, and CVV in a .env file and loaded them securely using python-dotenv.

One of the main challenges was that the login form appeared in a modal with an overlay that blocked interaction. I resolved this by removing the overlay using JavaScript. Another issue was that the form fields and buttons sometimes weren’t interactable due to how the page was structured. I solved this by scoping all element lookups inside the modal and using a .submit() fallback in case the purchase button wasn’t clickable.

I scheduled the script using cron to run at 8:00 AM on weekdays, since my laptop is already open and active at that time. This avoids needing to keep a Python process running constantly, as would be required with the schedule module.

During development, I added logging and screenshot debugging to identify issues step by step. Once everything was working, I cleaned up the script for production.
