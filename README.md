# MarkeTeller

Empowering Investors: Discover Stocks, Generate Reports, and Make Informed Decisions with AI-Powered Insights.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
- [Contact](#contact)

## Introduction

MarkeTeller is a web application that harnesses the power of algorithms and AI to assist investors in making informed decisions about stocks. The app's algorithm scans the stock market, identifies potential investment opportunities, and then leverages ChatGPT to automatically generate detailed reports on those stocks. Whether you're a novice investor or an experienced trader, StockReportAI provides insights and predictions that can help you navigate the stock market more confidently.

## Features

- **Stock Discovery:** Our algorithm searches the stock market to uncover stocks with potential for growth or value.
- **Automated Reports:** ChatGPT generates comprehensive reports on selected stocks, providing insights into the company, its financials, and recent market trends.
- **Predictive Analysis:** Get AI-powered predictions about the potential future performance of selected stocks.
- **User-Friendly Interface:** An intuitive web interface makes it easy to input preferences, view generated reports, and make investment decisions.


## Getting Started

Follow these steps to get started with MarkeTeller.

### Prerequisites

- [MongoDB](https://docs.mongodb.com/manual/installation/) set up and running.
- A valid API key from [financialmodelingprep.com](https://financialmodelingprep.com/developer/docs/) to access financial data.
- An API key for ChatGPT from OpenAI. [Sign up](https://beta.openai.com/signup/) for access.


### Installation

Follow these steps to set up the StockReportAI Web App on your local machine:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/DaveDushi/MarkeTeller.git
   cd MarkeTeller
2. Install the required Python packages using pip:

   ```bash
   pip install -r requirements.txt

### Configuration

MarkeTeller comes with a `config.json` file located in the `backend` folder. This file is pre-configured to hold your API keys and MongoDB URI. Follow these steps to set up your configuration:

1. Navigate to the `backend` folder:

   ```bash
   cd .\BackEnd

2. Open the `config.json` file in a text editor.

3. Replace the placeholders with your actual API keys from financialmodelingprep.com and OpenAI, as well as your MongoDB URI:

   ```json
   {
    "api_key": "your_financialmodelingprep_api_key_here",
    "db_uri": "your_mongodb_uri_here",
    "api_key_GPT": "your_openai_api_key_here"
    }
4. Save the config.json file.

### Usage

Once you've completed the installation and configuration steps, you're ready to start using MarkeTeller. Follow these steps to explore stocks, generate reports, and gain valuable insights:
1. Run the Flask development server:

   ```bash
   cd .\BackEnd
   flask --app main run
2. Open another terminal and launch the React app

    ```bash
   cd .\FrontEnd\my-app
   npm install 
   npm start
3. After you've started the React development server using npm start, you can open your web browser and navigate to http://localhost:3000 and use the app freely

   
## Contact

If you have any questions, suggestions, or feedback regarding MarkeTeller, please feel free to get in touch:

- **Email**: [david.dusi@hotmail.com](mailto:your.email@example.com)
- **GitHub**: [DaveDushi](https://github.com/YourGitHubUsername)
- **LinkedIn**: [david-d-929172208](https://www.linkedin.com/in/YourLinkedInProfile)


We appreciate your interest and input! Your feedback helps us improve and enhance the app for a better user experience.
