# Portfolio Optimizer

## A fast api to optimize your portfolio  

This API allows users to optimize a portfolio of tickers based on historical data.  
<p align="center">
    <img src="./datas/efficient_frontier.png"
         alt="Efficient Frontier graph">
</p>

## Efficient frontier

Efficient frontier optimization is a method used in finance to find the optimal portfolio of assets that provides the highest expected return for a given level of risk or the lowest risk for a given level of expected return. It involves calculating the expected returns and covariance matrix of a set of assets, and then finding the set of portfolios that lie on the efficient frontier, which represents the best possible trade-off between expected return and risk. This optimization method can be used to construct portfolios that are well-diversified and optimized for a specific level of risk tolerance or investment objective.

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#download">Download</a> •
  <a href="#credits">Credits</a> •
  <a href="#related">Related</a> •
  <a href="#license">License</a>
</p>

Portfolio Optimizer API  

## How To Use
The API is deployed on render.com, on <a href="https://portfolio-optimizer.onrender.com/">https://portfolio-optimizer.onrender.com/</a> 
  > **Note**
  > Check the status of the API on Render.com by visiting the API's homepage or status page.  
If the API is currently offline or unavailable, wait for it to wake up.
This may take a few minutes or more, depending on the reason for the outage.
Once the API is awake and running, you can start making requests to it as usual.

API Endpoints
Root
Endpoint to check if the API is running.  
Request:

```sql
GET /
```

Response:

```json
{
  "message": "Welcome to Portfolio Optimizer!"
}
```

<p align="center">
<img src=".\datas\fast_api.png" alt="efficient frontier" align="center"> 
</p>

Tickers
Endpoint to optimize a portfolio of tickers.

Request:

```sql
POST /tickers/
```

Parameters:

The POST request body is a JSON format with two keys:  

tickers: a list of strings containing the tickers of the assets in the portfolio.  
weights: a list of integers containing the weights of the assets in the portfolio.  

You can test it on the post tab of the api documentation, or using an api client like thunderclient or postman.

<p align="center">
<img src=".\datas\Query_render.png" alt="efficient frontier" align="center"> 

</p>
<p align="center">
<img src=".\datas\Query.png" alt="efficient frontier" align="center"> 
</p>

Response:

If successful, the endpoint returns a JSON object containing the optimized portfolio and URLs to two graphs:

```json
{
    "portfolio": {
        "return": 0.07834263983865495,
        "volatility": 0.10597974076381088,
        "sharpe_ratio": 0.7377197342857546,
        "weights": [
            0.2843565124085234,
            0.2647558605077321,
            0.06261841747241835,
            0.2588443351981374,
            0.1294248744131898
        ]
    },
    "graphs": {
        "efficient_frontier": "/graphs/efficient_frontier.png",
        "weights": "/graphs/optimisation_plot.png"
    }
}
```


If there is an error, the endpoint returns a JSON object with an error message:

- Please remove similar tickers!  
- Please check the sum of weights is equal to 100!  
- Tickers [ticker1, ticker2] do not exist!  
- Not enough historical data for those tickers: [ticker1], please remove them from the tickers list.  

Graphs
Endpoint to access static graph files.

Request:

```sql
GET /graphs/efficient_frontier.png
GET /graphs/optimisation_plot.png
```

Response:

A static image file.
<table border="0">
 <tr>
    <td><p style="font-size:1em" align="center">Efficient frontier</b></td>
    <td><img src=".\datas\efficient_frontier.png" alt="efficient frontier" align="center"></td>
 </tr>
 <tr>
    <td><p style="font-size:1em" align="center">Portfolio optimisation</b></td>
    <td><img src=".\datas\optimisation_plot.png" alt="graph from clustering model" align="center"></td>
 </tr>
</table>

The efficient frontier graph shows:  

- the position of the actual portfolio in orange,  
- the best return portfolio in red,  
- the minimum risk portfolio in green,  
- the portfolio optimizing the return for the actual risk, in blue (verticla arrow),  
- the porfolio reducing the risk for the actual return (horizontal arrow).  

The portfolio optimisation graph shows the weights for each portfolio.  

 

### Dependencies  

Python 3.8 or higher  
FastAPI  
NumPy  
Pandas  
SciPy  
Matplotlib  

## Key Features

* Deployed on render
  - https://portfolio-optimizer.onrender.com/docs
  - https://portfolio-optimizer.onrender.com/docs
  - https://portfolio-optimizer.onrender.com/docs
  - https://portfolio-optimizer.onrender.com/docs
  - https://portfolio-optimizer.onrender.com/docs
  - https://portfolio-optimizer.onrender.com/docs
* Sync Scrolling
  - While you type, LivePreview will automatically scroll to the current location you're editing.
* GitHub Flavored Markdown  
* Syntax highlighting
* [KaTeX](https://khan.github.io/KaTeX/) Support
* Dark/Light mode
* Toolbar for basic Markdown formatting
* Supports multiple cursors
* Save the Markdown preview as PDF
* Emoji support in preview :tada:
* App will keep alive in tray for quick usage
* Full screen mode
  - Write distraction free.
* Cross platform
  - Windows, macOS and Linux ready.


To clone and run this application, you'll need [Git](https://git-scm.com) and [Node.js](https://nodejs.org/en/download/) (which comes with [npm](http://npmjs.com)) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/amitmerchant1990/electron-markdownify

# Go into the repository
$ cd electron-markdownify

# Install dependencies
$ npm install

# Run the app
$ npm start
```



## Download

You can [download](https://github.com/amitmerchant1990/electron-markdownify/releases/tag/v1.2.0) the latest installable version of Markdownify for Windows, macOS and Linux.

## Emailware

Markdownify is an [emailware](https://en.wiktionary.org/wiki/emailware). Meaning, if you liked using this app or it has helped you in any way, I'd like you send me an email at <bullredeyes@gmail.com> about anything you'd want to say about this software. I'd really appreciate it!

## Credits

This software uses the following open source packages:

- [Electron](http://electron.atom.io/)
- [Node.js](https://nodejs.org/)
- [Marked - a markdown parser](https://github.com/chjj/marked)
- [showdown](http://showdownjs.github.io/showdown/)
- [CodeMirror](http://codemirror.net/)
- Emojis are taken from [here](https://github.com/arvida/emoji-cheat-sheet.com)
- [highlight.js](https://highlightjs.org/)

## Related

[markdownify-web](https://github.com/amitmerchant1990/markdownify-web) - Web version of Markdownify

## Support

<a href="https://www.buymeacoffee.com/5Zn8Xh3l9" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

<p>Or</p> 

<a href="https://www.patreon.com/amitmerchant">
	<img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" width="160">
</a>

## You may also like...

- [Pomolectron](https://github.com/amitmerchant1990/pomolectron) - A pomodoro app
- [Correo](https://github.com/amitmerchant1990/correo) - A menubar/taskbar Gmail App for Windows and macOS

## License

MIT

---

> [amitmerchant.com](https://www.amitmerchant.com) &nbsp;&middot;&nbsp;
> GitHub [@amitmerchant1990](https://github.com/amitmerchant1990) &nbsp;&middot;&nbsp;
> Twitter [@amit_merchant](https://twitter.com/amit_merchant)

