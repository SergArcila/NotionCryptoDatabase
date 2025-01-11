# Notion Crypto Portfolio Tracker

This repository contains a Python script that **automatically fetches live crypto prices from CoinMarketCap** and updates a **Notion database** with those prices (and optionally calculates a holding value). It’s especially useful for anyone who wants to track their cryptocurrency holdings directly in Notion without manually updating prices.

## Features

- **Automated Price Updates**  
  Fetches live market data for your tokens/coins from the CoinMarketCap API.

- **Notion Integration**  
  Updates a specified Notion database table with the latest price—no manual data entry needed.

- **Customizable Decimal Formatting**  
  Truncates or rounds token prices for readability, especially for tokens with many leading zeros.

- **Rate Limiting/Delay**  
  Includes optional delays or retry logic to avoid hitting CoinMarketCap’s rate limits (HTTP 429 errors).

## How It Works

1. You have a **Notion database** with columns for:
   - **Name** (title)
   - **Symbol** (text property, e.g., “BTC,” “ADA,” etc.)
   - **Amount** (number property, how many tokens you hold)
   - **Price** (number property, updated by the script)
   - **Current Holding Value** (a formula or number property if you want the script to calculate total value)

2. The **Python script**:
   - Uses your **Notion Integration Token** to access the Notion API.
   - Uses your **CoinMarketCap API key** to pull the latest price.
   - Loops over each row in your database, grabs the coin symbol, fetches its price, and updates Notion.

3. An **optional GitHub Actions workflow** can run this script on a schedule (e.g., daily at 8 AM UTC), so your Notion prices stay up to date automatically.

## Getting Started

### 1. Clone or Fork the Repository

```bash
git clone https://github.com/<your-username>/<this-repo>.git
cd <this-repo>

