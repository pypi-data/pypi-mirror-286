import { Widget } from '@lumino/widgets';
import { ShowThemeDetail } from './showthemedetail';


export class ForumDashboardWidget extends Widget {

    private originalHTML: string; // Declare the property
    private activeTab: string = 'all'; // Track the active tab

    constructor() {
        super();

        this.originalHTML = `
            <header>
                <!--NavBar Section-->
                <div class = "navbar">
                    <div class="forum-title">Databrix Lab Forum</div>
                </div>
            </header>
            <div class="container">
              <div class="tabs">
                <button class="tab" data-tab="all">All</button>
                <button class="tab" data-tab="open">Open</button>
                <button class="tab" data-tab="closed">Closed</button>
              </div>
              <div class="subforum">
                <div class="subforum-title">
                  <h1>General Information</h1>
                </div>
                <div id="themes-container"></div>
              </div>
            </div>
            `;
        this.node.innerHTML = this.originalHTML; // Set initial HTML
        this.fetchAndDisplayThemes();

        // Event listener for "Description Title" link
        this.node.addEventListener('click', (event) => {
            const target = event.target as HTMLElement; // Get the clicked element

            if (target.classList.contains('tab')) {
              this.activeTab = target.dataset.tab ?? 'all'; // Default to 'all' if undefined
              this.updateTabDisplay();
            }

            if (target.classList.contains('description-link')) { // Check if it's the correct link
                const ThemeID = target.getAttribute('data-description-id');
                event.preventDefault(); // Prevent default link behavior
                ShowThemeDetail(this, ThemeID);
            }
        });
    }


    private async fetchAndDisplayThemes() {

        // Fallback example themes declared outside of try-catch block
        const exampleThemes = [
            {
              ThemeID: 1,
              Title: "Example Theme 1",
              Author: "Admin",
              CreationTime: "2024-07-01T10:00:00",
              Status: "open"
            },
            {
              ThemeID: 2,
              Title: "Example Theme 2",
              Author: "User123",
              CreationTime: "2024-07-15T15:30:00",
              Status: "closed"
            }
        ];

        try {
            const response = await fetch('https://1985609f-7839-4819-8840-2d38548e4ea5.ma.bw-cloud-instance.org/jupyterhub/services/forum/');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            const themes = data.themes;

            const themesContainer = this.node.querySelector('#themes-container');
            if (themesContainer) {
                themesContainer.innerHTML = themes.map((theme: any) => `
                    <div class="subforum-row">
                        <div class="subforum-description subforum-column">
                            <h4><a href="#" class="description-link" data-description-id="${theme.ThemeID}">${theme.Title}</a></h4>
                            <p>Created by ${theme.Author} on ${new Date(theme.CreationTime).toLocaleDateString()}</p>
                            <p>Status: ${theme.Status}</p>
                        </div>
                        <div class="subforum-info subforum-column">
                            <b><a href="#">Posted</a></b> by <a href="#">${theme.Author}</a>
                        </div>
                    </div>
                    <hr class="subforum-devider">
                `).join('');
            }
        } catch (error) {
            console.error('Error fetching themes:', error);

            const themesContainer = this.node.querySelector('#themes-container');
            if (themesContainer) {
                themesContainer.innerHTML = exampleThemes.map((theme: any) => `
                    <div class="subforum-row">
                        <div class="subforum-description subforum-column">
                            <h4><a href="#" class="description-link" data-description-id="${theme.ThemeID}">${theme.Title}</a></h4>
                            <p>Created by ${theme.Author} on ${new Date(theme.CreationTime).toLocaleDateString()}</p>
                            <p>Status: ${theme.Status}</p>
                        </div>
                        <div class="subforum-info subforum-column">
                            <b><a href="#">Posted</a></b> by <a href="#">${theme.Author}</a>
                        </div>
                    </div>
                    <hr class="subforum-devider">
                `).join('');
            }
        }
    }

    private updateTabDisplay() {
      const allThemes = [...this.node.querySelectorAll('.subforum-row')];

      allThemes.forEach(theme => {
        const themeElement = theme as HTMLElement;

        // Ensure the element exists and has textContent before splitting
        const lastChildParagraph = themeElement.querySelector('p:last-child');
        const status = lastChildParagraph && lastChildParagraph.textContent
                        ? lastChildParagraph.textContent.split(': ')[1] || ''
                        : '';  // Default to empty string if not found

        if (this.activeTab === 'all' || status === this.activeTab) {
          themeElement.style.display = 'grid';
        } else {
          themeElement.style.display = 'none';
        }
      });
    }

}
