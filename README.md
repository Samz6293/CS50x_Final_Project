# 💰 Expense Tracker

#### Video Demo: [<URL HERE>](https://youtu.be/kxEZ6vtkcCY)

#### Description:

A command-line expense tracking application built with Python and SQLite that allows multiple users to manage their personal expenses with an intuitive menu-driven interface.

## Overview

Expense Tracker is a multi-user financial management tool designed to help individuals track their spending habits across different categories. The application provides a clean, emoji-enhanced interface that makes expense management both functional and visually appealing. Users can add expenses, categorize them, view spending patterns, and manage their transaction history—all from a simple terminal interface.

## Features

### Core Functionality

- **Multi-User Support**: Create and manage multiple user profiles, each with independent expense tracking
- **Expense Management**: Add, view, and delete expenses with detailed information
- **Category-Based Tracking**: Organize expenses by custom categories (e.g., Food, Transport, Entertainment)
- **Total Calculation**: View aggregate spending per user
- **Optional Notes**: Attach descriptive notes to transactions for better record-keeping
- **Timestamp Tracking**: Automatic recording of when expenses and users are created

### User Interface

- Clean, decorated table outputs using the `tabulate` library
- Emoji-enhanced prompts and feedback messages
- Validation for all user inputs
- Confirmation dialogs for destructive operations
- Menu-driven navigation with 8 primary options

## Project Structure

```
expense-tracker/
│
├── expenses.py          # Main application file with all core functions
├── helpers.py           # Helper functions for UI decoration and exit handling
├── requirements.txt     # Python package dependencies
├── expenses.db          # SQLite database (created on first run)
└── README.md            # This file
```

### File Descriptions

#### `expenses.py`

The main application file containing all primary functionality:

- **`main()`**: Entry point that displays the menu and routes user choices to appropriate functions
- **`add_expense()`**: Handles the creation of new expense records with validation for user ID, category, amount, and optional notes
- **`view_expenses()`**: Displays all expenses for a selected user in chronological order
- **`view_by_category()`**: Shows available categories for a user and filters expenses by selected category
- **`view_total()`**: Calculates and displays the sum of all expenses for a specific user
- **`delete_expense()`**: Removes a transaction after user confirmation
- **`add_user()`**: Creates new user profiles with unique names
- **`delete_user()`**: Removes users and all associated expense data with warning prompts
- **`valid_id()`**: Helper function to validate user ID input against the database
- **`valid_category()`**: Helper function to ensure category input is not empty
- **`all_users()`**: Displays all registered users in a formatted table

#### `helpers.py`

Contains utility functions for consistent UI presentation:

- **`decorate_top()`**: Prints top border for standard-width tables
- **`decorate_top_long()`**: Prints top border for wide tables
- **`decorate_bottom()`**: Prints bottom border for standard-width tables
- **`decorate_bottom_long()`**: Prints bottom border for wide tables
- **`exit_now()`**: Provides option to continue or quit after completing an action

#### `requirements.txt`

Lists the Python packages required to run the application:
- `cs50`: Provides the SQL class for database interactions
- `tabulate`: Enables formatted table output

## Database Design

The application uses SQLite with two main tables:

### `users` Table

| Column     | Type     | Constraints                |
|------------|----------|----------------------------|
| id         | INTEGER  | PRIMARY KEY, AUTOINCREMENT |
| name       | TEXT     | UNIQUE, NOT NULL           |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP  |

### `expenses` Table

| Column     | Type     | Constraints                       |
|------------|----------|-----------------------------------|
| id         | INTEGER  | PRIMARY KEY, AUTOINCREMENT        |
| user_id    | INTEGER  | NOT NULL, FOREIGN KEY → users(id) |
| category   | TEXT     | NOT NULL                          |
| amount     | REAL     | NOT NULL, CHECK (amount > 0)      |
| note       | TEXT     | (optional)                        |
| expense_at | DATETIME | DEFAULT CURRENT_TIMESTAMP         |

The database enforces referential integrity through the foreign key relationship between `expenses.user_id` and `users.id`, ensuring data consistency across user deletions.


## Usage

1. **Run the application**:
   ```bash
   python expenses.py
   ```

2. **Navigate the menu** by entering numbers 1-8:
   - **1. Add Expense**: Record a new expense for a user
   - **2. View All**: See all expenses for a selected user
   - **3. By Category**: Filter expenses by category
   - **4. View Total**: Display total spending for a user
   - **5. Delete Expense**: Remove a specific transaction
   - **6. Add User**: Create a new user profile
   - **7. Delete User**: Remove a user and all their data
   - **8. Exit**: Close the application

3. **Example workflow**:
   - Start by adding a user (option 6)
   - Add expenses for that user (option 1)
   - View expenses by category (option 3) or see totals (option 4)
   - Delete unwanted transactions (option 5) if needed

## Design Decisions

### Why SQLite?

SQLite was chosen for its simplicity and zero-configuration setup. For a command-line application with a single user at a time, SQLite provides all necessary database functionality without the overhead of a server-based system.

### Why Multi-User Support?

While this is a command-line tool, multi-user support enables:

- Families to track expenses for different members
- Small businesses to separate employee expenses
- Individual users to maintain separate budget categories (personal vs. business)

### Input Validation Strategy

The application implements defensive programming by validating all user inputs:
- User IDs are verified against the database
- Amounts must be positive numbers
- Categories cannot be empty
- Destructive operations require confirmation

This approach prevents database errors and provides clear feedback to users.

### UI/UX Choices

The application uses `tabulate` for clean table formatting and emojis for visual feedback. While emojis may not render consistently across all terminals, they enhance user experience on modern systems and make the application more engaging.

The `exit_now()` function after each operation allows users to continue working or quit at natural breakpoints, reducing unnecessary menu navigation.

## Future Enhancements

Potential improvements for future versions:
- Export functionality (CSV, PDF reports)
- Data visualization (charts, graphs)
- Web app functionality
- Recurring expense management
- Currency conversion support
- Search functionality across all expenses
