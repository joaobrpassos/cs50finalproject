# Title:  CS50chan

#### Video Demo:  https://youtu.be/if5jLmWZu4A?si=zr3vXhRQ-M3k_NTZ

#### Description:
**CS50chan** is an imageboard forum-style website created with Flask, CSS, and Bootstrap. Inspired by traditional anonymous imageboards, it provides a streamlined platform for anonymous discussions, allowing users to post, reply, and interact with content across multiple dynamically generated boards.

### Key Features
CS50chan incorporates several features that make it a functional and user-friendly imageboard platform. Here’s a breakdown of each core feature and its functionality:

1. **Posting and Replying**
   - Users can create new posts with a title, content, and an optional file attachment (usually an image) to start conversations. Replies to posts consist of content and optional files, facilitating ongoing discussion and interaction.
   - Each post and reply receives a unique identifier, allowing users to refer to and quote previous posts for clearer conversation flow.

2. **User Ban Management by IP**
   - Moderators (superusers) can manage site behavior by banning or unbanning users based on their IP address. Banned users receive a message explaining their restriction and are prevented from posting or replying.
   - This feature helps maintain a respectful environment by enabling moderators to address rule-breaking behavior effectively.

3. **Dynamic Moderator Control**
   - Superuser privileges are controlled at the code level by an ID list. This simple mechanism allows administrators to designate or revoke superuser status dynamically, adjusting site permissions as needed.
   - Superusers have broader control over posts and users, allowing for a balance between community moderation and user freedom.

4. **Self-Deletion of Posts**
   - Users can delete only their own posts, promoting personal accountability and maintaining user control over their contributions.
   - Superusers, however, retain the authority to delete any post if necessary, further supporting effective moderation and content management.

5. **Anonymous Posting with User Identification**
   - CS50chan preserves user anonymity while assigning each user a unique identifier linked to their IP address. This system enables users to participate without revealing their personal information while still providing traceable identity for accountability.
   - Identifiers help differentiate users in ongoing conversations, adding structure and clarity to the anonymous forum environment.

6. **Dynamic Board Creation**
   - CS50chan supports the creation of new boards through a simple function, `board()`, which accepts three parameters:
     - **endpoint** (URL endpoint for the board, e.g., "/b"),
     - **name** (full board title and description, e.g., "/b/ - Random and Memes"),
     - **bname** (short name or board abbreviation, e.g., "b").
   - This feature offers administrators flexibility in expanding the site with new thematic boards, allowing for a diverse range of discussion topics without extensive configuration.

7. **Post Timestamping**
   - The date and time of each post are displayed alongside the content, allowing users to see when posts were made. This timestamp feature improves conversation flow and makes it easier to reference posts in a temporal context.

8. **Unique Post and Reply Numbers**
   - Each post and reply is assigned a distinct number, simplifying referencing and quoting. Users can mention specific posts by number in replies, which helps maintain clarity and continuity in discussions, particularly in longer threads.

### Technologies and Design Choices
CS50chan utilizes several core technologies and design principles that make it functional, efficient, and user-friendly:

- **Flask** provides the backend functionality, managing requests, routing, and database interactions for smooth user experience and efficient data handling.
- **CSS** and **Bootstrap** are used to create a clean and responsive front-end design, offering users an intuitive and visually appealing interface.
- **SQLite** serves as the database, supporting data storage for posts, user information, and board settings.

### Use Cases
Here are some examples of how users might engage with CS50chan and utilize its features:

- **Anonymous Discussion**: Users can start conversations without creating accounts, fostering open, candid discussions across various topics.
- **Moderation and Control**: Superusers manage boards effectively by banning disruptive users and deleting inappropriate posts, ensuring a safe environment.
- **Custom Board Creation**: Administrators can quickly add new boards to accommodate growing topics of interest, supporting a scalable, dynamic forum structure.

### Security and Privacy Considerations
CS50chan handles user anonymity carefully, storing minimal user information and relying on IP-based identification for moderation purposes. Moderators have restricted access to user data, ensuring privacy remains a priority. IP-based user banning and identification are implemented to prevent spam and maintain order without compromising user anonymity.

### Future Improvements
While CS50chan is a functional prototype, additional features could enhance its usability and security:

- **Enhanced Moderator Tools**: Adding options like post editing, content filtering, or word bans would further empower superusers to maintain order.
- **User Experience Enhancements**: Adding features like post upvoting, image previews, or thread archiving would improve user engagement.
- **Database Optimization**: Migrating to a more scalable database like PostgreSQL would enhance performance for larger deployments.
- **Spam Protection**: Implementing CAPTCHA or rate-limiting could prevent spam and improve site security.

---

With a strong foundation and rich feature set, **CS50chan** brings traditional imageboard functionality into a modern, Flask-based platform, offering an accessible, scalable solution for anonymous discussion and community-building.
