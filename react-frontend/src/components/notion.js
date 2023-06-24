const oauth_client_id = "abc0a276-2e19-48a0-bd69-d84e6228b73d";

export const LoginNotion = ({dbs}) => {
    return (
        <div>
        <a
            style={{ display: "block" }}
            href={`https://api.notion.com/v1/oauth/authorize?client_id=${oauth_client_id}&response_type=code&owner=user&redirect_uri=http%3A%2F%2Flocalhost%3A3000`}
        >
            Connect to Notion
        </a>
        {dbs.map((db) => (
            <div>
            <h3>データベース：
                <a
                href={db.url}
                >
                {db.title.map(part => part.plain_text).join('')}
                </a>
            </h3>
            </div>
        ))}
        </div>
    );
}
