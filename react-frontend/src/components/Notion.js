import { InputText } from "./InputText";

const oauth_client_id = "abc0a276-2e19-48a0-bd69-d84e6228b73d";

export const LoginNotion = ({dbs}) => {
    if (dbs[0] === undefined) {
        return (
        <div>
                <a
                    style={{ display: "block" }}
                    href={`https://api.notion.com/v1/oauth/authorize?client_id=${oauth_client_id}&response_type=code&owner=user&redirect_uri=http%3A%2F%2Flocalhost%3A3000`}
                >
                    Connect to Notion
                </a>
        </div>
        );
    };
    return (
        <div>
        <a
            style={{ display: "block" }}
            href={`https://api.notion.com/v1/oauth/authorize?client_id=${oauth_client_id}&response_type=code&owner=user&redirect_uri=http%3A%2F%2Flocalhost%3A3000`}
        >
            Connect to Notion
        </a>
        <div>
            <h3>データベース：
                <a
                style={{ display: "block" }}
                href={dbs[0].url}
                >
                {dbs[0].title.map(part => part.plain_text).join('')}
                </a>
            </h3>
        </div>
        </div>
    );
}

export const AddNotionPage = ({dbs}) => {
    const handleSubmit = (e) => {
        e.preventDefault();
        const url = e.target.url.value;
        fetch(`http://localhost:5000/add-page?url=${url}`, {credentials: 'include'}).then(async (resp) => {
            const data = await resp.json();
            console.log(data);
        });
    };
    return (
        <div>
            <InputText handleSubmit={handleSubmit}/>
        </div>
    );
}