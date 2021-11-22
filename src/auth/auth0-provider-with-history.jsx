import React from "react";
import { useHistory } from "react-router-dom";
import { Auth0Provider } from "@auth0/auth0-react";

const reactAppDomain = process.env.REACT_APP_DOMAIN;

const Auth0ProviderWithHistory = ({ children }) => {
  const domain = process.env.REACT_APP_AUTH0_DOMAIN;
  const clientId = process.env.REACT_APP_CLIENT_ID;

  const history = useHistory();
  const scope = "read:attendees update:attendees create:attendees delete:attendees " +
                "read:groups update:groups create:groups delete:groups " +
                "read:events update:events create:events delete:events"

  const onRedirectCallback = (appState) => {
    history.push(appState?.returnTo || window.location.pathname);
  };

  return (
    <Auth0Provider
      domain={domain}
      clientId={clientId}
      redirectUri={reactAppDomain}
      //redirectUri={"https://hbdatracking.azurewebsites.net/home"}
      //redirectUri={"http://localhost:3000/home"}
      audience={"https://hbda-tracking-backend.azurewebsites.net"}
      scope={scope}
      onRedirectCallback={onRedirectCallback}
    >
      {children}
    </Auth0Provider>
  );
};

export default Auth0ProviderWithHistory;
