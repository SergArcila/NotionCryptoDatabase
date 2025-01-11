# Notion Crypto Portfolio Tracker

This repository contains a Python script that **automatically fetches live crypto prices from CoinMarketCap** and updates a **Notion database** with those prices (and optionally calculates a holding value). It’s especially useful for anyone who wants to track their cryptocurrency holdings directly in Notion without manually updating prices. If you are anything like me, you have 100 different coins accross a million different locations so here you can take note where all your coins are stored as well. 

## PREREQS

You need a notion database. You need to get a few important pieces of information. You need NOTION_TOKEN, NOTION_DATABASE_ID and CMC_API_KEY. If you have questions text me 786-203-9240. Here is my notion template so duplicate it and fill it out with your coin and the correct information.
https://dull-eyelash-ccc.notion.site/178ef5bb9f7280168674eb67216bd317?v=f8de439eabdf4e1b9f2762a0ecab12f8&pvs=4

PS. now you know what coins I actively have haha.

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
   - **Location of Asset** (Where your coins are for easy tracking)

2. The **Python script**:
   - Uses your **Notion Integration Token** to access the Notion API.
   - Uses your **CoinMarketCap API key** to pull the latest price.
   - Loops over each row in your database, grabs the coin symbol, fetches its price, and updates Notion.

3. An **optional GitHub Actions workflow** can run this script on a schedule (e.g., daily at 8 AM UTC), so your Notion prices stay up to date automatically.

## Getting Started

### 1. Clone or Fork the Repository

You got this. Ask chat.

