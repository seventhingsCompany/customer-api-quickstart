# Authentication

All starters share these variables:

| Variable | Meaning |
| --- | --- |
| `SEVENTHINGS_INSTANCE_URL` | Instance root URL, required |
| `SEVENTHINGS_TOKEN` | Existing bearer token, preferred when set |
| `SEVENTHINGS_USERNAME` | Username for password authentication |
| `SEVENTHINGS_PASSWORD` | Password for password authentication |
| `SEVENTHINGS_CLIENT_ID` | OAuth client ID for password authentication |

If the token is absent or empty, all three credential variables are required. SDK credential helpers authenticate before recipe execution. `hello` additionally calls ping, field discovery, and object listing. Ping alone does not establish that authentication works.

The starters are short-lived CLI programs. Long-running integrations must implement token expiry/refresh using the selected SDK's authentication service and returned expiry information. SSO is supported by the SDKs, but acquiring an authorization code belongs to the host application's login flow; see the matching SDK documentation before adding it.

`.env.example` documents configuration. Source a locally edited `.env` from your shell or use your application's environment loader. Never commit tokens or print login responses. For browser applications, use an appropriate user authentication flow; keep password-based service credentials on a backend.
