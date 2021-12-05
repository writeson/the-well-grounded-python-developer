/**
 * This self-invoking JavaScript function populates the 
 * hidden timezone info field in the login form
 */
(function() {
  let timezone_info = document.getElementById('timezone_info');
  timezone_info.value = JSON.stringify(Intl.DateTimeFormat().resolvedOptions());
}())
