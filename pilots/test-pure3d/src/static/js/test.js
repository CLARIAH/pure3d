function changeUserRole(key, value) {
  // Get the existing data from the form
  var formData = new FormData();
  formData.append('key', key);
  formData.append('value', value);

  // Make an AJAX request to the Flask server to update the value in the YAML file
  fetch('/update_user_role', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    // If the update was successful, update the value on the webpage
    if (data.success) {
      // Find the corresponding element on the page and update its text
      var elem = document.getElementById(key);
      elem.querySelector('.value').textContent = value;
    } else {
      console.error(data.error);
    }
  })
  .catch(error => console.error(error));
}


function change_Status(key,value)
{
  // Get the existing data from the form
  var formData = new FormData();
  formData.append('key', key);
  formData.append('value', value);

  // Make an AJAX request to the Flask server to update the value in the YAML file
  fetch('/update_status', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    // If the update was successful, update the value on the webpage
    if (data.success) {
      // Find the corresponding element on the page and update its text
      var elem = document.getElementById(key);
      elem.querySelector('.value').textContent = value;
    } else {
      console.error(data.error);
    }
  })
  .catch(error => console.error(error));
}
