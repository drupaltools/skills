# Example 01

> Drupal multilingual website with SDC components.

**Agile way of working**
(each website section had its own Mockups, Site Structure, Theming etc):

- We found ourselves doing a lot of multitasking.
- The design system and design components were changing over time so more complex Components had to be created.
- Too many options appeared for Editors on Drupal that can break the UI (e.g. too many button options, compinations of layouts etc). 

**SDC components and theming**

- Key module: Drupal core sdc
- Since this was a new method of working on Drupal we spent a lot of time to decide the process and files structure.
- Did some mistakes on SDC components that could not revert on later (e.g. wrong attributes types, embed VS incude on twig, not using slots, overusing components)
- SDC needs a Drupal instance so our Stylers were still on a need for a Drupal live website
- Storybook features were not used as much as we could for UI testing
- We spend a lot of work for the complex Components like navigation and form items.
- Naming Components is a very important task.
- Figma Dev mode was turned into a paid service (it was free) before ending the project. This affected the Developers a bit when creating Components.
- CSS should be more "cascade" especially for global variables and utility classes.
- CSS should not have duplicate styles.
- We have our "ready to use" SDC theme for future projects.
- The module cl_server was deprecated before ending the development. We did not have the time to move on the new, suggested module storybook so our Stories are currently on yml.

**Drupal**

- We should better use Drupal bundle (PHP) classes instead of hooks etc to alter/extend Drupal fields.
- We had too many issues with f*ile names and file paths* while migrating.
- Too many "fixes" had to be done on Drupal entities due to changed requirements from the Agile process.
- Sometimes we offer t*oo many (similar) options to Editors* to create content (e.g. through a CKEditor template, a normal Drupal field or through Paragraphs).
- Search API indexing on a single SOLR core is a task we somehow do not "control". Too many problems appear still on Search that need advanced investigation.
- We did not study the 7.x request logs before switching to 10.x so we had some suprises (e.g. too many bot requests).
- The hosting system of Acquia Cloud is a system we do not manage either can tune as we prefer so we sometimes are stacked on it (e.g. on broken deployments)
- A new module created (a migration source plugin the migrates files by field and bundle) and will be published on Drupal.org modules.

**Theming**

- The mockups were based on a design system but I spent a lot of time integrating the tokens and css variables.
- It was complicated because each component had a separate CSS file and that was the problem that caused the css variables duplications. I preferred to use Sass variables and less CSS variables. Next time I suggest keeping all css files in the same directory.
- There were times where the storybook components were styled and on the live site were broken due to an overridden style or different HTML. That's why we preferred to test it on the live site.
- It was difficult to style the landing pages because they were created at the last minute with the final content.
- It would be better if we had more mockups, especially for the landing pages before starting the implementation.
- We gave too many panel combinations and in the end, we used less.
- We should have an accessibility and performance test upfront.
