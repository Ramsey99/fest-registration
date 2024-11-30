# Contributing to Fest Registration

Thank you for your interest in contributing to the **Fest Registration** project! We appreciate any help to improve the project and make it better for everyone. Follow the instructions below based on whether you use **GitHub Desktop** or the **Command Prompt** to get started.

---

## Prerequisites
- Ensure that you have **[Node.js](https://nodejs.org/)** installed.
- Install **[Git](https://git-scm.com/)** for command prompt users.

---

## For GitHub Desktop Users

### 1. **Fork the Repository**
- Navigate to the repository on GitHub.
- Click on the **Fork** button at the top-right corner to create your own copy of the repository.

### 2. **Clone the Repository Locally**
- Open **GitHub Desktop**.
- Go to **File > Clone Repository**.
- Select the repository you forked from your GitHub account.
- Choose the local directory where the repository will be saved.
- Click **Clone**.

### 3. **Install Dependencies**
- Open the repository in your preferred code editor.
- In the terminal, run the following command to install dependencies:

    ```bash
    npm install
    ```

### 4. **Set Up the Development Environment**
- If the project requires environment variables, set them up using an `.env` file.
- You can find a sample configuration in the `.env.example` file.

### 5. **Running Tests and Development Tasks**
- Run tests to ensure everything works:

    ```bash
    npm test
    ```

- Start the development server to view the project locally:

    ```bash
    npm start
    ```

---

## For Command Prompt Users

### 1. **Fork the Repository**
- Navigate to the repository on GitHub.
- Click the **Fork** button at the top-right corner to create your own copy.

### 2. **Clone the Repository Locally**
- Open **Command Prompt** or terminal.
- Run the following command to clone the repository (replace `your-username` with your GitHub username):

    ```bash
    git clone https://github.com/your-username/fest-registration.git
    cd fest-registration
    ```

### 3. **Install Dependencies**
- Install the project dependencies by running the following command:

    ```bash
    npm install
    ```

### 4. **Set Up the Development Environment**
- Configure the environment variables in an `.env` file.
- Refer to the `.env.example` file for guidance.

### 5. **Running Tests and Development Tasks**
- Run the following command to test the project:

    ```bash
    npm test
    ```

- Start the development server locally using:

    ```bash
    npm start
    ```

---

## Submitting Your Contribution

### 1. **Create a New Branch**
- **GitHub Desktop Users:**
  - In **GitHub Desktop**, go to **Branch > New Branch** and name it (e.g., `feature-new-functionality`).
- **Command Prompt Users:**
  - Run the following command to create a new branch:

    ```bash
    git checkout -b feature-new-functionality
    ```

### 2. **Make Your Changes**
- Implement your changes in the new branch.
- Ensure you follow coding standards and conventions.

### 3. **Commit Your Changes**
- **GitHub Desktop Users:**
  - In **GitHub Desktop**, go to **Commit**, add a descriptive message, and commit your changes.
- **Command Prompt Users:**
  - Use the following command to commit your changes:

    ```bash
    git add .
    git commit -m "feat: add new functionality to the registration form"
    ```

### 4. **Push Your Branch**
- **GitHub Desktop Users:**
  - Click **Push Origin** in GitHub Desktop to push your branch to your forked repository.
- **Command Prompt Users:**
  - Run the following command to push your branch:

    ```bash
    git push origin feature-new-functionality
    ```

### 5. **Submit a Pull Request**
- Go to the original repository on GitHub.
- Click **New Pull Request**.
- Select your branch and provide a description of the changes.
- Submit the pull request for review.

---

## Best Practices

- Follow coding style guidelines and best practices.
- Ensure your commits are clear and organized.
- Test your changes thoroughly before submitting.
- Keep pull requests focused on one issue or task.

Thank you for contributing to **Fest Registration**!
