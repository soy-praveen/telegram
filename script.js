// Initialize the Telegram Web App
const telegram = window.Telegram.WebApp;

// Extract all available data from initDataUnsafe
const user = telegram.initDataUnsafe.user || {};
const platform = telegram.platform;
const themeParams = telegram.themeParams || {};
const initData = telegram.initData || "No initData available";
const isPremium = user.is_premium ? "Yes" : "No";
const isBot = user.is_bot ? "Yes" : "No";

// Format user details
const userInfo = `
    ID: ${user.id || "Not available"}
    Username: ${user.username || "Not available"}
    First Name: ${user.first_name || "Not available"}
    Last Name: ${user.last_name || "Not available"}
    Language Code: ${user.language_code || "Not available"}
    Is Premium: ${isPremium}
    Is Bot: ${isBot}
`;

// Format platform and theme details
const platformInfo = `
    Platform: ${platform || "Unknown"}
    Theme Params: ${JSON.stringify(themeParams, null, 2)}
`;

// Format other details
const otherInfo = `
    Init Data: ${initData}
    Auth Date: ${telegram.initDataUnsafe.auth_date || "Not available"}
    Hash: ${telegram.initDataUnsafe.hash || "Not available"}
`;

// Update the HTML with extracted details
document.getElementById("user-info").innerText = userInfo;
document.getElementById("platform-info").innerText = platformInfo;
document.getElementById("other-info").innerText = otherInfo;

// Notify Telegram that the Web App is ready
telegram.ready();
