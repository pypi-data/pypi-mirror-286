export async function ShowThemeDetail(widget: any, ThemeID: any) {


    // Example theme data
    const exampleTheme = {
      Title: "Example Theme",
      Description: "This is an example theme description.",
      Author: "User123",
      CreationTime: "2024-07-24T10:08",
      Replies: [
        { Author: "Example Author2", Content: "This is an example reply to the theme2.", CreationTime: "2024-07-22T10:08" },
        { Author: "Example Author", Content: "This is an example reply to the theme.", CreationTime: "2024-07-24T10:08" },
      ]
    };

    try {
        // Make a POST request to retrieve the theme details
        const response = await fetch('https://1985609f-7839-4819-8840-2d38548e4ea5.ma.bw-cloud-instance.org/jupyterhub/services/forum/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ThemeID: ThemeID }),
        });

        const themeDetail = await response.json();

        // Update the widget's HTML to display the theme details
        widget.node.innerHTML = `
          <div class="topic">
            <div class="topic-header">
              <h2 class="topic-title">${themeDetail.Title}</h2>
              <div class="topic-meta">
                <span class="topic-author">by ${themeDetail.Author}</span>
                <span class="topic-date">${new Date(themeDetail.CreationTime).toLocaleDateString()}</span>
              </div>
            </div>

            <div class="topic-body">
              <div class="topic-content">${themeDetail.Description}</div>
              <div class="topic-stats">
                <span>${themeDetail.Replies.length} Antworten</span> •
              </div>
            </div>

            <div class="topic-replies">
              <h3>Antworten</h3>
              <div class="replies-container">  </div>
            </div>

            <button id="back-to-forum" class="btn btn-primary">Back to Forum</button>
          </div>
        `;
        // Insert replies into replies-container
        const repliesContainer = widget.node.querySelector('.replies-container');
        themeDetail.Replies.forEach((reply: any) => {
            const replyDiv = document.createElement('div');
            replyDiv.className = 'reply';
            replyDiv.innerHTML = `
              <div class="reply-header">
                <span class="reply-author">${reply.Author}</span> •
                <span class="reply-date">${new Date(reply.CreationTime).toLocaleDateString()}</span>
              </div>
              <div class="reply-content">${reply.Content}</div>
            `;
            repliesContainer?.appendChild(replyDiv); // Add the reply div to the container
          });

        const backButton = widget.node.querySelector('#back-to-forum');
        backButton?.addEventListener('click', () => {
            widget.node.innerHTML = widget.originalHTML;
            widget.fetchAndDisplayThemes();
        });
    } catch (error) {
        console.error('Error fetching theme details:', error);
        // Update the widget's HTML to display the theme details
        widget.node.innerHTML = `
          <div class="topic">
            <div class="topic-header">
              <h2 class="topic-title">${exampleTheme.Title}</h2>
              <div class="topic-meta">
                <span class="topic-author">by ${exampleTheme.Author}</span>
                <span class="topic-date">${new Date(exampleTheme.CreationTime).toLocaleDateString()}</span>
              </div>
            </div>

            <div class="topic-body">
              <div class="topic-content">${exampleTheme.Description}</div>
              <div class="topic-stats">
                <span>${exampleTheme.Replies.length} Antworten</span> •
              </div>
            </div>

            <div class="topic-replies">
              <h3>Antworten</h3>
              <div class="replies-container">  </div>
            </div>

            <button id="back-to-forum" class="btn btn-primary">Back to Forum</button>
          </div>
        `;

        // Insert replies into replies-container
        const repliesContainer = widget.node.querySelector('.replies-container');
        exampleTheme.Replies.forEach((reply: any) => {
            const replyDiv = document.createElement('div');
            replyDiv.className = 'reply';
            replyDiv.innerHTML = `
              <div class="reply-header">
                <span class="reply-author">${reply.Author}</span> •
                <span class="reply-date">${new Date(reply.CreationTime).toLocaleDateString()}</span>
              </div>
              <div class="reply-content">${reply.Content}</div>
            `;
            repliesContainer?.appendChild(replyDiv); // Add the reply div to the container
          });

        const backButton = widget.node.querySelector('#back-to-forum');
        backButton?.addEventListener('click', () => {
            widget.node.innerHTML = widget.originalHTML;
            widget.fetchAndDisplayThemes();
        });
    }
}
