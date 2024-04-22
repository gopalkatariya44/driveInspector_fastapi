
// Function to convert UTC time to local time
function convertUTCToLocal(utcTimeString) {
  // Create a Date object from the UTC time string
  var utcDate = new Date(utcTimeString);

  // Convert the UTC time to local time
  var localDate = new Date(utcDate.getTime() + utcDate.getTimezoneOffset() * 60000);

  // Format the local date to desired format
  var options = { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: true };
  var formattedDate = localDate.toLocaleString('en-US', options);

  // Return the formatted local date
  return formattedDate;
}

// Example UTC time string
const utcTimeStr = "{{detection_details['created_at']}}";

// Convert UTC time to local time and display it
document.getElementById("created_at").innerHTML = convertUTCToLocal(utcTimeStr);
