# Travel-Split-Money

## Project Overview

This Travel-Split-Money System is a Streamlit web application designed to facilitate the management of financial transactions among a group of members. It allows for adding members, recording transactions including who paid and who owes money, and calculating the debt relationships based on these transactions.

## Features

*   **Add Members**: Users can input the names of members participating in transactions.
*   **Record Transactions**: Record details of financial transactions including item names, amounts, payer, and optional notes.
*   **Split Costs**: During transaction recording, the application allows splitting the cost of the transaction among multiple members.
*   **Calculate Debts**: The application calculates and displays the debt relationship, showing how much each member owes or is owed.

## Technologies Used

*   Python
*   Streamlit
*   Pandas (for handling data frames)
*   Dataclasses (for defining data models)

## How to Run the Application

1. **Setup Python Environment**: Ensure Python 3.x is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2. **Install Dependencies**: Open your terminal and install the required Python libraries using pip:

   `pip install streamlit pandas`

3. **Run the Application**: Navigate to the directory containing the application files (`app.py` and `models.py`), and run the following command:

   `streamlit run app.py`

4. **Open Web Application**: After running the command, your terminal will display a local URL, usually `http://localhost:8501`, where you can access the application through your web browser.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
