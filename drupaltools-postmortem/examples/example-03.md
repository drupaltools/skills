# Example 03

> Drupal portal with GraphQL API and mobile App connected to Drupal

#### Drupal website

**New things learned**

- Use Drupal GraphQL for the API
- Implement the `graphql_compose` Drupal module
- Create many custom `graphql_compose`-based modules (see ACEW-22 and [https://jira.eworx.gr/issues/?jql=labels%20%3D%20graphql](https://jira.eworx.gr/issues/?jql=labels%20%3D%20graphql))
- Publish some of the modules on Drupal.org (see ACEW-22)
- Removing a content or entity type in Social (e.g. Post type) is almost impossible
- Social deeply alters forms and Drupal routes, so implementing features requires excessive caution

**Challenges and how they were solved**

- Drupal hooks are not passed to the GraphQL API
- Created Drupal services to reuse functionality both in hooks and API
- Drupal code deployments must always be coordinated with Mobile App deployments
- API stability must be maintained
- Decided not to remove Drupal fields to prevent breaking older app versions
- To keep the Mobile App as agnostic as possible, the API exposed not only collections/values but also Drupal Form API and several CRUD-like routes, in an agnostic “get only what you need” way

**New modules or software created**

- Yes, several Drupal modules were created and published.

**Reusability of the codebase**

- Yes, the Drupal modules and methodology allow reuse in other projects
- Approximately 90% data-agnostic
- Remaining 10% depends on project-specific content types, mainly affecting GraphQL Views

**What we would change if starting over**

- Avoid installing Social distribution as-is
- Prefer selectively installing only certain Social modules
- Maintaining Social plus an API on top of it is too difficult
- With so many hooks, we should consider using the upcoming Drupal 11 hook system via the Drupal 10 class `core/lib/Drupal/Core/Hook/Attribute/Hook.php`
- Implement Unit Testing from day one

#### React Native with GraphQL API

**New things learned**

- Use React Native GraphQL with Apollo Client
- Use Recycle List View for large complex lists
- Use React Native Calendars for event integration
- Use `d3-interpolate-path` for custom SVG animations

**Challenges and how they were solved**

- The mobile app required too much dynamic content provided via API
- Required extensive processing across nearly all screens
- YouTube links in posts caused issues
- Created a custom module to extract video IDs

**New modules or packages created**

- Yes, a custom Drupal module for extracting YouTube IDs
- Useful for packages like `react-native-youtube-iframe`

**Reusability of the codebase**

- The mobile app code is 100% reusable

**What we would change if starting over**

- Reduce the amount of dynamic content to improve performance
- Avoid designing the mobile app as if it also needed to be a responsive web app
