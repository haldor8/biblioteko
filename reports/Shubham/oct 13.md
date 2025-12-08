Worked on the Secaniors
Wrote the Sceaniors 
Reviwed to the professor

not a final output: 

# Application Installation:
   
Description: Describes the process of installing the application on different media.
Actors: The user, the server providing the application.
Precondition: The application must be available for download from the user's media (computer or smartphone).
Steps:
1. The future user opens their browser or the market store of their operating system.
2. The future user types in the name of the application.
3. The selection page displays the description of the application and its legal information, including details related to the sharing of works and copyright rights.
4. The future user selects the application and installs it.

# Become a Member
   
Description: An anonymous user
Actors: An anonymous user, FranceConnect, and the various agents of FranceConnect.
Prerequisite: The "Install the application" scenario has been executed without error.
Steps:

1. The anonymous user launches the application.
2. The application detects that this is the first launch on the device.
3. The application displays an information page.
4. The application offers the user the option to log in via FranceConnect.
5. The application offers the option to create an account that cannot upload or rent works.
6. The user chooses to log in via FranceConnect.
7. The application offers different identification sites.
8. The user selects one of the sites.
9. The user authenticates themselves.
10. The application receives the login information.
11. The application displays all available actions, including uploading.

Alternative scenario:
(Branching from step 6)
1. The user chooses to create a new identifier.
2. The application requests the user’s first name, last name, and date of birth.
3. The user enters the information.
4. Using this information, the application creates:
- A unique identifier ensuring anonymity,
- A pair of keys, public and private, to record future operations.

5. The application transmits the identifier and the public key to the association’s server.
6. The application displays the allowed actions.
7. The application displays a list of works in the public domain.

Documents:

Information page displayed: to explain the objective of the application, its features, and clarifies that the user will need to use a FranceConnect account if they want to rent works under copyright or upload works.


# Become a Librarian

Description: A member requests to become a librarian.
Actors: Member, Librarian
Prerequisite: There is at least one active librarian.

Steps:

1. A member requests through the application to become a librarian.
2. The application registers the request and submits it to the librarians.
3. The application on another librarian's device sends the request to the user for moderation.

4. The application asks the librarian if they:

- accept,

- reject,

- have no opinion,

5. or wish to ignore the application.
6. The librarian indicates their choice to the application.
7. The application shares this choice anonymously and uniquely with other applications on the devices of other librarians.
8. The librarian can modify their choice as long as the given deadline has not passed.
- Once the deadline has passed, the librarians' applications propagate the automatic decision to other applications as follows:

9. If the majority of librarians have accepted the member's application, the member becomes a librarian.
10. The member checks the decision from the application on their device.
11. If the future librarian’s application detects that they have been promoted to librarian, they receive the rights to access all content and to accept or reject moderations.

Otherwise, the application indicates that their promotion has been rejected.

Alternative scenarios:

The majority of librarians reject the promotion.

Error scenarios:

Data, documents, screens:

# Log in to the library

Description: Authenticates a user to access their personal space.
Actors: User, authentication server.
Preconditions: The user account must exist and be activated.

Steps
1. The user opens the application.
2. The user enters their login credentials.
3. The server verifies the information.
4. The user is redirected to their dashboard.

# Access the list of works

Description: Allows browsing and searching for works in the library.

Actors: User.

Preconditions: The user is logged in, and the library contains published works.
Steps:
1. The user accesses the "Catalog" section.
2. They can filter by type (books, music, videos, articles), by category, or by keywords.
3. The application displays the list of available works.
4. The user selects a work to view its detailed information (title, author, description, rights, format, availability).

# Submit a digitized work

Description: A member has digitized a work and wishes to share it with the library to enrich its collection.
Actors: Authenticated member
Prerequisite: The member is authenticated in the application via FranceConnect.

Steps:
1. The authenticated member requests the application to share a work.
2. The application displays a form to input information about the work.
3. The authenticated member enters the information and attaches the digitized file of the work.
4. The application requests confirmation of the submission.
5. The authenticated member confirms the submission.
6. The application saves the file in the "to be moderated" directory.
7. The application creates a transaction number and records it in the local log file.
8. The application sends the file, its information, and the transaction numbers to the server of the association for deposit.
9. The association’s servers notify the librarians that a new work is pending moderation.
10. The application notifies the member that their submission is pending moderation.

Alternative scenarios:
Error scenarios:

  Connection error with the server.

# Moderate a digitized work

Description: Librarians are notified of digitized works pending moderation.

Actors: Librarian, National Library of France server.

Prerequisite: The file of a digitized work must have been submitted and is awaiting moderation.

Steps:

1. One of the librarians logs into the application.
2. The application displays the list of digitized work files that have been submitted.
3. The librarian sets their filters to only see works that might interest them.
4. The application displays only the results that match the filters.
5. The librarian sets the sorting criteria to display the works in the desired order.
6. The application displays the results in the selected order.
7. The librarian selects a file for a work.
8. The application displays the information entered by the member who submitted the work.
9. The application displays a reader specific to the file type.
10. The librarian reviews the work.
11. The librarian completes the information for the work.
12. The librarian accepts the work, specifying its nature.

Alternative scenarios:

Error scenarios:

Data, documents, screens:

# View a work in the public domain

Description: Allows a user to view and read a work that belongs to the public domain directly from the library.
Actors: User, library server.
Preconditions:

The user is logged into the application (or accesses as a guest if open access is allowed).
The work is classified as "public domain" and validated by a librarian.

Steps:

1. The user accesses the "Catalog" or "Shared Collection" section.
2. The user selects a work that is public domain.
3. The server displays the full details of the work (title, author, date, summary, format).
4. The user clicks on "Read online" or "Download."
5. The file is displayed in the integrated reader or downloaded locally.

# Fill in information about a work

Description: Allows a member who uploads a work to complete the metadata necessary for its classification.

Actors: Member (work uploader), server, Git repository.

Preconditions:

The work file has been uploaded in the "Propose a Work" section.
The user is authenticated.

Steps:

1. The member accesses the upload form.
2. They enter the required information:

   * Title, author, year, category, language, type of work, copyright status.
3. The server checks the consistency of the data (format, required fields).
4. The metadata is saved in **metadata.yml** associated with the work.
5. A message confirms that the information has been successfully recorded.

# Consult information concerning a work

Description: Allows viewing the metadata and status of a work present in the library.

Actors: User, server.
Preconditions:

The work exists in the library.
The user is logged in or has public access.

Steps:

1. The user searches for a work via the search engine or catalog.
2. The user selects the desired work.
3. The server displays the detailed record (title, author, categories, description, availability, rights type, submission date).
4. The user can also view the link to the Markdown file or the OCR text.

# Edit information about a work

Description: Allows a librarian or administrator to edit the metadata of a work after moderation.

Actors: Librarian, administrator.

Preconditions:

The user has modification rights.
The work is already recorded in the Git repository.

Steps:

1. The librarian accesses the work’s record.
2. The librarian clicks on "Edit Information."
3. The librarian updates one or more fields in the **metadata.yml** file.
4. The server validates the changes (format, consistency of rights).
5. A new version is saved in the Git repository (commit).
6. The modification history is updated and can be viewed.

# Rent a copyrighted work

Description: Allows a member to temporarily borrow a work protected by copyright.

Actors: Member, application server, encryption service, Git repository.

Preconditions:

The user is logged in and has a valid account.
The work is available for rental.

Steps:

1. The user selects a copyrighted work.
2. The user clicks on "Rent this work."
3. The server creates a specific encryption key and encrypts the file.
4. The key is encrypted with the member's public key (creating **key.enc**).
5. The file is added to **emprunts/<user-id>/<work-id>/**.
6. The rental duration (14 days) is recorded in the metadata database.
7. After the rental period expires, the file becomes inaccessible and access is revoked.


# Passage of a work into the public domain

Description: Automatically manages the transition of a copyrighted work to the public domain when the rights expire.

Actors: System, librarian (final validation).

Preconditions:

The copyright protection end date has been reached.
The metadata contains copyright information.

Steps:

1. The system regularly checks works under copyright.
2. It detects works whose protection period has expired.
3. An automatic report is generated for the librarian.
4. The librarian confirms or cancels the status update.
5. The work is moved to the **fond_commun/** directory.
6. A notification is sent to the members.

# Distribution of a royalty-free work

Description: Allows the system to automatically propagate a work that has become free to all members with shared space.

Actors: Server, subscribed members.

Preconditions:

The work is classified as "rights-free" or has recently entered the public domain.
Members have enabled automatic synchronization.

Steps:

1. The system detects a new free work.
2. It creates a copy in **fond_commun/**.
3. The server synchronizes this work to the shared spaces of the members.
4. A notification informs users of the availability.
5. The work becomes viewable and downloadable from their interface.







