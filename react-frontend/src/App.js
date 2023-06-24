import './App.css';
import { useEffect, useState } from "react";

// The OAuth client ID from the integration page!
const oauth_client_id = "abc0a276-2e19-48a0-bd69-d84e6228b73d";

const LoginNotion = ({dbs}) => {
  return (
    <div>
      <a
        style={{ display: "block" }}
        href={`https://api.notion.com/v1/oauth/authorize?client_id=${oauth_client_id}&response_type=code&owner=user&redirect_uri=http%3A%2F%2Flocalhost%3A3000`}
      >
        Connect to Notion
      </a>
      {dbs.map((db) => (
        <div
          style={{
            display: "inline-flex",
            whiteSpace: "pre",
            border: "1px solid black",
            marginBottom: 10,
          }}
        >
          {JSON.stringify(db, null, 2)}
        </div>
      ))}
    </div>
  );
}

function App() {
  const [dbs, setdbs] = useState([]);

  // When you open the app, this doesn't do anything, but after you sign into Notion, you'll be redirected back with a code at which point we call our backend.
  useEffect(() => {
    const params = new URL(window.document.location).searchParams;
    const code = params.get("code");
    console.log(code);
    if (!code) return;
    fetch(`http://localhost:5000/login/${code}`).then(async (resp) => {
      setdbs(await resp.json());
    });
  }, []);

  return (
    <div className="App">
      <h1>Paper to Notion</h1>
      <LoginNotion dbs={dbs}/>
    </div>
  );
}

export default App;
