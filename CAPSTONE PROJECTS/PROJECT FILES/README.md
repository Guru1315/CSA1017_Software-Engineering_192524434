# Project files

Four files from the **Mini AI Software Dev Team** project: a team of AI agents (Product Manager, Architect, Developer and Tester) that turns a feature request into a spec, a design, code and a test report. The `(1)` in the file names is what browsers add to repeated downloads, and the console's download buttons produce files called `app.py` and `software-dev-team-output.md`.

| File | What it is |
|---|---|
| `index (1).html` | **Dev Team Console**, a single-page web app to run the team, watch each agent's output arrive live, edit each agent's prompt, model and temperature, and download the results |
| `supabase (1).sql` | The Supabase database script behind the console: tables `agent_config`, `runs` and `run_steps`, live updates, and starter prompts for the four agents |
| `software-dev-team-output (1).md` | A sample final output from the team for a password strength checker CLI: a spec, a design, the code and a test report that ends with `VERDICT: PASS` |
| `app (1).py` | A command-line to-do app with `add`, `list` and `delete` commands. It matches the example request used in the Develop-Team README, "a CLI to-do app in Python with add, list, and delete" |

## How the pieces fit

```
Dev Team Console (index.html)  --POST {run_id, request}-->  n8n webhook  -->  four AI agents
        ^                                                                           |
        |__ reads agent settings and live results from Supabase  <-- writes each step __|
```

`index (1).html` and `supabase (1).sql` are identical to `web/index.html` and `web/supabase.sql` in the [Develop-Team repository](https://github.com/Guru1315/Develop-Team/tree/main/web), where the n8n workflow changes and the setup steps are written out in `web/README.md`. The console does not work on its own: it needs a Supabase project and an n8n webhook.

## Running the console

1. Create a Supabase project and run `supabase (1).sql` in its SQL Editor.
2. Open `index (1).html` in a browser.
3. Enter the Supabase project URL, the **anon** (public) key and the n8n webhook URL, then click **Save & connect**. Never enter the `service_role` key in the page.
4. Type a request and click **Run**.

The keys are kept in your browser's local storage, and **Clear saved keys** removes them.

## The to-do app

`app (1).py` uses only the Python standard library and stores tasks in a `tasks.json` file next to the script. It creates that file on the first `add`.

```bash
python "app (1).py" add "Buy milk"
python "app (1).py" list
python "app (1).py" delete 1
```

Empty descriptions and unknown task IDs print an error and exit with code 1. The sample output file describes a different program (the password checker), so the two come from separate runs of the team.

## Security note

The database policies in `supabase (1).sql` allow anyone who has the page and your anon key to read and change the data. That is fine for a class demo, but add Supabase Auth and tighten the policies before real use. The n8n webhook is also public unless you add authentication to it.
