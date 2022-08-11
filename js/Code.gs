// TODO: Replace URL with your own URL (no trailing slash)
const baseUrl = "URL";
const token = ScriptApp.getOAuthToken();

function updateStripeDashboard() {
  runPython(baseUrl + "/stripe/dashboard", { apiKey: token });
}
