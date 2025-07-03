const { createAppAuth } = require("@octokit/auth-app");
const { Octokit } = require("@octokit/core");
const fs = require("fs");

const APP_ID = process.env.APP_ID;
const PRIVATE_KEY = fs.readFileSync("private-key.pem", "utf8");

(async () => {
  const auth = createAppAuth({
    appId: APP_ID,
    privateKey: PRIVATE_KEY,
  });

  const appAuthentication = await auth({ type: "app" });

  const octokit = new Octokit({ auth: appAuthentication.token });

  const res = await octokit.request("GET /app/installations");
  res.data.forEach(i => {
    console.log(`Installation ID: ${i.id} | Account: ${i.account.login} | Repositories: ${i.repository_selection}`);
  });
})();
