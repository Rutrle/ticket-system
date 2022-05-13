<div class="container p-5">
    <div class="container bg-dark p-5">
        <div>
            <h1>Welcome to the Smart Ticket</h1>
            <hr>
            <p>Aim of this project was creating a ticketing website system, with flask backend and SQLlite database. For
                frontend were used mainly Bootstrap5 templates.</p>
            <p>Main purpose of this project is for me to get better with flask framework - because of this many of
                things that could be probably done better on frontend are done in backend</p>
            <p>Apart from CRUD interface for creating and manipulating tickets this project also includes handling user
                profiles and sending automatical e-mails</p>
            <p>Project also contains script for resetting database and filling it with dummy data - <b>db_setup.py</b></p>
            <p> You can find the website running on following <a href="https://rutrle.pythonanywhere.com/">link</a>
            <hr>
            <h3>Used libraries:</h3>
            <ul>
                <li><b>Poetry</b> for libraries managment</li>
                <li><b>Flask</b> for website backend</li>
                <li><b>Flask-SQLAlchemy</b> for database setup and communication</li>
                <li><b>WTForms</b> for forms and forms validation</li>
                <li><b>CKEditor</b> rich text editor</li>
                <li><b>bcrypt</b> for hashing passwords</li>
                <li><b>phonenumbers</b> for validating phone numbers</li>
                <li><b>Pillow</b> for resizing profile pictures</li>
                <li><b>faker</b> for for creating dummy data</li>
            </ul>
            <hr>
        </div>
        <div>
            <h1>How does the website work?</h1>
            <hr>
            <h3>Not logged in/unregistered</h3>
            <p>There is not much of the website functionality you can access without logging in/registering</p>
            <p>
                In the navbar, you can click onto following links:
            </p>
            <ul>
                <li>
                    <b>"SmartTicket"</b> which will take you to the home page
                </li>
                <li>
                    <b>"About"</b> ,which will take you to page with information about this website
                </li>
                <li>
                    <b>"New Ticket"</b> ,which will allow you to create new support ticket in rich text editor, however
                    as you are not logged in, author of it will be anonymous
                </li>
                <li>
                    <b>"Login"</b> ,which will take you to the page where you can log in with existing account. If you
                    have forgoten your password, you can reset your password and let it be sent to your e-mail.
                </li>
                <li>
                    <b>"Register"</b> ,which will allow you to create new account. Althought it's not required to enter
                    your real e-mail, SmartTicket has e-mail sending functionalities, so it's higly recommended to use a real
                    one which you can access. Registering will create a standard user account for you.
                </li>
            </ul>
            <hr>
            <h3>Logged in as standard user</h3>
            <p>When you register and login as standard user you will be able to access most of the SmartTicket
                functionality</p>
            <p>You will be able to create, update and solve tickets</p>
            <p>You will be able to add tickets that interest you into your <b>watchlist</b> and <b>start solving</b>
                them by adding yourself as one of the current solvers</p>
            <p>You will recieve e-mails about tickets that you are solving or are on your watchlist when they are
                updated, solved, or reopened</p>
            <p>You will be able to update your account information, like e-mail, profile picture, password...</p>
            <p>There will be now more possibilitis in your navbar, although <b>"SmartTicket" and "About"</b> will remain
                the same, the rest:</p>
            <ul>
                <li>
                    <b>Landing page</b> You will be taken to this page right after logging in.
                    It displays tickets that are on your watchlist and those which you are currently solving, so it acts
                    as overview of tickets that are important for you
                </li>
                <li>
                    <b>New ticket</b> works mostly the same as if you would not be logged in, however when you create a
                    ticket, you will be marked as its author
                </li>
                <li>
                    <b>Unresolved tickets</b> This page contains paginated list of all tickets that have been not yet
                    solved. You can order and filter it with several parameters.
                    In every ticket record you can find a button with magnifying glass icon. It will take you to the
                    ticket detail page.
                    <ul>
                        in <b>Ticket detail</b> you can see and do several things:
                        <li>
                            You can see basic info about the ticket - when it was created, it's whole text, who is
                            currently solving it etc.
                        </li>
                        <li>
                            You can add the ticket to your <b>watchlist</b> or you can start <b>solving</b> it
                        </li>
                        <li>
                            You can see and contribute to tickets <b>message log</b> in which are kept all records about
                            what was done with the ticket - from information about its creation,
                            to various updates from other users detailing what they were doing towards solving it and
                            when the ticket is solved than also info about its solution
                        </li>
                        <li>
                            You can also <b>solve ticket</b> on this page, which marks you as its solver
                        </li>
                    </ul>
                </li>
                <li>
                    <b>Archive</b> leads to page almost the same as "unresolved tickets", with exception that you can
                    see here all already solved tickets (for example if you are solving similar one, you can look how it
                    was solved)
                </li>
                <li>
                    <b>Your account name</b> leads to page containing details about your user account.
                    <ul>
                        <p>In user account details you can see information about user like contact info, profile picture
                            and what he or she is currently solving</p>
                        <p>In case it's your account, you can go to profile update page where you can change your
                            profile information, profile picture and your password </p>
                    </ul>
                </li>
                <li>
                    And finally <b>Logout</b> logs you out of the Smart Ticket
                </li>
            </ul>
            <hr>
            <h3>Logged in as admin</h3>
            <p>User accounts with <b>administrator</b> rights can acces some more functionalitis in addition to all a
                standard user can</p>
            <p>As this is only demonstration version, you can try it out with default admin user - both username and
                password is "admin"</p>
            <p>Administrators acces their functionalities through <b>Administrator tools</b> in their navbar, there are
                two:</p>
            <ul>
                <li>
                    <p><b>User administration</b></p>
                    <p>
                        In here you can see all users, some of their details like when their account was created, if
                        they
                        are standard user or administrator and so on. You can also <b>deactivate</b> their account (so
                        the
                        can't log in and use SmartTicket), or <b>change their user role</b> (promote standard user to
                        admin and
                        vice versa). You can also <b>reactivate</b> already deactivated user profile.
                    </p>
                </li>
                <li>
                    <p><b>Ticket administration</b></p>
                    <p>
                        In here you can see all tickets, both solved and unresolved. Apart from functionality that
                        standard user can also access you can <b>reopen</b> already solved ticket, or completely
                        <b>delete</b> on of the tickets.
                    </p>
                </li>
            </ul>
        </div>
    </div>
</div>