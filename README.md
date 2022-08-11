# Stripe Dashboard for Google Sheets and Microsoft Excel

![Screenshot](/screenshot.png?raw=true)

An xlwings remote interpreter sample app showing you how to build your own Stripe dashboard directly in Google Sheets or Microsoft Excel. The users of the spreadsheet don't need to have Python installed locally. Requires xlwings PRO (commercial use requires an xlwings subscription while non-commercial use is free).

## Supported Spreadsheets

This app is compatible with:

* Google Sheets
* Desktop Excel on Windows
* Desktop Excel on macOS
* Excel on the web

## Server quickstart

The easiest way to try things out is by clicking the Deploy to Render button below and filling in the required environment variables in the Render dashboard (this makes use of Render's free tier).

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

You'll be asked to provide the following environment variables:

* `GOOGLE_ALLOWED_DOMAINS` (make sure to format like a Python list): `["your_workspace_domain.com"]`
* `XLWINGS_LICENSE_KEY` (get a [trial key](https://www.xlwings.org/trial)): `your_xlwings_pro_license_key`
* `STRIPE_API_KEY`: `your_stripe_api_key_or_restricted_key`
* `XLWINGS_API_KEY`: `set_to_a_strong_random_key`

> Note:
> * Leave `GOOGLE_ALLOWED_DOMAINS` empty if you don't want to use Google Sheets
> * Leave `XLWINGS_API_KEY` empty if you don't want to use Microsoft Excel

Instead of deploying to Render, you can deploy this app to any provider that can deal with a Dockerfile or Python. You could also run the server locally via `python run.py` and expose it via a service like ngrok, see the [remote interpreter docs](https://docs.xlwings.org/en/stable/remote_interpreter.html).

## Spreadsheets

## Google Sheets

* Copy the template by clicking on `Use Template`: https://docs.google.com/spreadsheets/d/13sAqZUwycob8A3mYOuOK9AYpepgCK1qJsSc2OIfER38/template/preview
* Go to `Extensions` > `Apps Script`. In the `Code.gs` module, adjust the `URL` to match your backend (e.g., use the URL of the Render service from above)
* Click the `Update` button to query the outstanding invoices
* If you want to update your data automatically, you can set up a Google Sheets Trigger

## Desktop Excel (Windows & macOS)

* Use the `xlwings-remote-stripe.xlsm` file in the root of this repo
* In the VBA editor (`Alt+F1`), adjust the `URL` and `apiKey`
* Click the `Update` button to query the outstanding invoices

## Excel on the web

* Upload `xlwings-remote-stripe.xlsm` to OneDrive or SharePoint
* Copy/paste the code under `js/main.ts` into the Office Scripts editor on the `Automate` tab and adjust the parameters of the `main` function (make sure to pick the correct file with the `.ts` extension, not `.js`)
* You will have to create the `Update` button by clicking on the 3 dots on the Office Script editor and selecting `+ Add Button`
* Click the created button to query the outstanding invoices
