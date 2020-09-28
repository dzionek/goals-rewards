/**
 * Entry-point for the React app.
 */

import React from "react"
import ReactDOM from "react-dom"
import axios from "axios"

import "../sass/style.scss"
import App from "./App"

axios.defaults.baseURL = window.location.protocol + '//' + window.location.host

ReactDOM.render(
    <App />,
    document.getElementById("app")
)