/* 
 * Environment variables
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'bonya.eu.auth0.com', // the auth0 domain prefix
    audience: 'coffeeapp', // the audience set for the auth0 app
    clientId: 'avYUnzN5yfs0W65LV4PSh3a91J0bbQ8f', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
