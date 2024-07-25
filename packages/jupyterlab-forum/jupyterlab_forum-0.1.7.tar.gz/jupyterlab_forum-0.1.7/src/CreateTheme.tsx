import { ShowThemeDetail } from './showthemedetail';

export async function handleCreateThemeClick(widget: any, username: string) {
  // Temporary HTML for theme creation form
  const createThemeFormHTML = `
    <h2>Create New Theme</h2>
    <div class="create-theme-form">
      <label for="themeTitle">Title:</label>
      <input type="text" id="themeTitle" name="themeTitle"><br><br>
      <label for="themeDescription">Description:</label>
      <textarea id="themeDescription" name="themeDescription"></textarea><br><br>
      <button id="submitThemeButton">Create</button>
    </div>
  `;

  widget.node.innerHTML = createThemeFormHTML; // Update widget's HTML

  // Event listener for "Create" button
  const submitThemeButton = widget.node.querySelector('#submitThemeButton');
  if (submitThemeButton) {
    submitThemeButton.addEventListener('click', async () => {
          const titleInput = widget.node.querySelector('#themeTitle') as HTMLInputElement;
          const descriptionInput = widget.node.querySelector('#themeDescription') as HTMLTextAreaElement;

          const newTheme = {
            Title: titleInput.value,
            Description: descriptionInput.value,
            Author: username,
            Status: "Open"
            // Add other relevant fields (e.g., Author, CreationTime)
          };

          try {
            // Send theme data to the server (e.g., using fetch)
            const response = await fetch('services/forum/', {
              method: 'POST',
              body: JSON.stringify(newTheme),
              headers: { 'Content-Type': 'application/json' },
            });

            if (response.ok) {
              // Theme created successfully
              // Optionally: Get the new theme ID from the response (if the server provides it)
              const data = await response.json();
              const newThemeId = data.ThemeID;

              ShowThemeDetail(widget, newThemeId); // Show the details of the new theme
            } else {
              // Handle errors here (e.g., display an error message in the widget)
              console.error('Failed to create theme:', response.status);
            }
          } catch (error) {
            console.error('Error creating theme:', error);
            // Handle errors here (e.g., display an error message in the widget)
          }
    });
  }
}
