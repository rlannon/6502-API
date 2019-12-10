/* jshint esversion: 8 */
/* jshint node: true */
/* jshint strict: true */
'use strict';

const API_URL = "rlannon.herokuapp.com/api/v1/6502/";

async function getData(url) {
    return fetch(url)
        .then(response => response.json())
        .catch(error => console.log(error));
}
