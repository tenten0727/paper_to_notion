import { LoginNotion, AddNotionPage } from './components/Notion';
import { useEffect, useState } from "react";

// The OAuth client ID from the integration page!

function App() {
    const [dbs, setdbs] = useState([]);
    const [code, setcode] = useState("");

  // When you open the app, this doesn't do anything, but after you sign into Notion, you'll be redirected back with a code at which point we call our backend.
    useEffect(() => {
        const params = new URL(window.document.location).searchParams;
        const code = params.get("code");
        if (!code) return;
        setcode(code);
    }, []);

    // When the code changes, we call our backend to get the databases.
    useEffect(() => {
        if (!code) return;
        setdbs([]);
        fetch(`http://localhost:5000/login/${code}`, {credentials: 'include'}).then(async (resp) => {
        const data = await resp.json().then(d => d.results);
        setdbs(data);

        // Save the databases to local storage
        localStorage.setItem("dbs", JSON.stringify(data));

        // Clear the code query parameter from the URL
        window.history.pushState({}, document.title, window.location.pathname);
        });
    }, [code]);

    // When the component mounts, we check if there are databases saved in local storage
    useEffect(() => {
        const storedDbs = localStorage.getItem("dbs");
        if (storedDbs) {
            setdbs(JSON.parse(storedDbs));
        }
    }, []);

    return (
        <div className="App">
        <h1>Paper to Notion</h1>
        <LoginNotion dbs={dbs}/>
        <AddNotionPage dbs={dbs}/>
        </div>
    );
}

export default App;
