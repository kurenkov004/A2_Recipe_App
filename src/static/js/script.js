function showHideAnalytics() {
  let x = document.getElementById("analytics_container");
  if (x.style.display === 'none') {
    x.style.display = 'block';
  } else {
    x.style.display = 'none'
  }
}

//add_recipe_form logic
(function () {
  // Retrieves the form element for adding a recipe by its ID.
  const addRecipeForm = document.getElementById('add_recipe_form');

  if (addRecipeForm) {
    // Retrieves the URL for posting the form data from a data attribute on the form.
    const postUrl = addRecipeForm.getAttribute('data-post-url');

    // Adds an event listener to handle the form submission.
    addRecipeForm.addEventListener('submit', function (e) {
      // Prevents the default form submission mechanism to handle the submission via JavaScript.
      e.preventDefault();

      // Creates a new FormData object, capturing the form's current values.
      const formData = new FormData(addRecipeForm);

      // Executes a fetch request to submit the form data to the server.
      fetch(postUrl, {
        method: 'POST', // Specifies the request method.
        body: formData, // Attaches the form data as the request body.
        headers: {
          // Includes a CSRF token in the request headers for security purposes.
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        credentials: 'same-origin' // Ensures cookies are sent with the request if the URL is on the same origin.
      })
      .then(response => response.json()) // Parses the JSON response from the server.
      .then(data => {
        // Checks if the server responded with a success status.
        if (data.status === 'success') {
          // Closes the recipe modal by hiding it.
          document.getElementById('add_recipe_modal').style.display = 'none';
          // Reloads the page to reflect any changes made by the form submission.
          window.location.reload();
        }
      }).catch(error => console.error('Error:', error)); // Logs any errors that occur during the fetch request.
    });
  }
});

// add_recipe modal functionality
(function () {
  // retrieves necessary HTML elements
  const addRecipeButton = document.getElementById('addRecipeButton');
  const addRecipeModal = document.getElementById('add_recipe_modal');

  //look for  'close' span element
  const closeModalSpan = addRecipeModal ? addRecipeModal.querySelector('.close') : null;

  //function to display add_recipe_modal
  const openAddRecipeModal = () => {
    if (addRecipeModal) {
      addRecipeModal.style.display = 'block';
    }
  }
  //function to hide add_recipe_modal
  const closeAddRecipeModal = () => {
    if (addRecipeModal) {
      addRecipeModal.style.display = 'none';
    }
  }
  //addRecipeButton functionality
  if (addRecipeButton) {
    addRecipeButton.addEventListener('click', openAddRecipeModal);
  }
  //closeModal functionality
  if (closeModalSpan) {
    closeModalSpan.addEventListener('click', closeAddRecipeModal);
  }
  //logic to hide modal if user clicks outside of it
  window.addEventListener('click', function (e) {
    if (e.target == addRecipeModal) {
      closeAddRecipeModal();
    }
  });
})

//function to update recipe
document.addEventListener('DOMContentLoaded',function () {
  //retrieve button element that opens updateModal
  const updateButton = document.getElementById('updateRecipeButton');

  if (updateButton) {
    //retrieve modal element that holds update logic & the close modal element
    const updateModal = document.getElementById('update_recipe_modal');
    const closeUpdateModal = document.querySelector('#update_recipe_modal .close');

    //logic to open the modal onClick of updateButton
    updateButton.addEventListener('click', ()=>{
      if (updateModal) {
        updateModal.style.display = 'block';
      }
    });
    //logic to close modal
    if (closeUpdateModal) {
      closeUpdateModal.addEventListener('click', ()=> {
        if (updateModal) {
          updateModal.style.display == 'none';
        }
      });
    }
    //logic to hide modal if user clicks outside of it
    window.addEventListener('click', (e)=> {
      if (e.target == updateModal) {
        updateModal.style.display = 'none';
      }
    });
  }
})

//deleting the recipe functionality
document.addEventListener('DOMContentLoaded', function () {
  //retrieving CSRF token necessary for POST requests
  const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Checks if the current cookie is the one we're looking for.
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break; // exit the looop once cookie is found
            }
        }
    }
    return cookieValue; // Return the found cookie value or null if not found.
  }

  //retrieve necessary DOM elements
  const deleteButton = document.getElementById('deleteRecipeButton');
  const deleteModal = document.getElementById('delete_recipe_modal');
  const closeDeleteModal = document.getElementById('closeDeleteModal');
  const confirmDeleteButton = document.getElementById('confirmDeleteButton');
  
  //display delete confirmation modal when "delete" button is clicked
  if(deleteButton) {
    deleteButton.addEventListener('click', ()=> {
      deleteModal.style.display = 'block';
    });
  }

  //close delete confirmation modal when "close" button is clicked
  if (closeDeleteModal) {
    closeDeleteModal.addEventListener('click', ()=> {
      deleteModal.style.display = 'none';
    });
  }

  //logic to hide modal if user clicks outside of it
  if (deleteModal){
    window.addEventListener('click', (e) => {
      if (e.target == deleteModal) {
        deleteModal.style.display ='none';
      }
    });
  }

  //confirm deletion
  if (confirmDeleteButton) {
    confirmDeleteButton.addEventListener('click', function () {
      const recipeId = deleteButton.dataset.recipeId; // Retrieve the recipe ID from the data-attribute

      if (confirmDeleteButton) {
        // Make a POST request to the server to delete the recipe
        fetch(`/delete/${recipeId}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken') // Include CSRF token for security
          },
          credentials: 'include' // Ensure credentials such as cookies are included with the request
        })
        .then(response => response.json()) // Parse the JSON response from the server
        .then(data => {
          if (data.status === 'success') {
            // Notify the user of successful deletion and redirect to the list page
            alert('Recipe successfully deleted.');
            window.location.href = "/list/";
          } else {
            // Alert the user of an error based on the message from the server
            alert(`Error: ${data.message}`);
          }
        }).catch(error => {
          // Log and alert the user of any errors that occurred during the fetch operation
          console.error('Error:', error);
          alert(`An error occurred: ${error}`);
        });
      } else {
        alert("You must click button to confirm.");
      }
    });
  }
})

//