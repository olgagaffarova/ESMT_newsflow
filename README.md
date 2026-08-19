# ESMT Rankings Intelligence — minimal online cron test

This is deliberately a thin infrastructure test. It proves that:

1. GitHub Actions can execute a notebook online;
2. the notebook can collect live publications;
3. generated data can be committed back to GitHub;
4. Streamlit can display the refreshed CSV without a separate API.

Only the official Corporate Knights WordPress API is enabled. More publishers should be added only after this complete path works reliably.

## Files

- `ESMT_Rankings_Intelligence_Cron_Test.ipynb` — live collector and persistence logic;
- `.github/workflows/daily_collection.yml` — manual and daily execution;
- `app.py` — minimal Streamlit interface;
- `data/` — generated CSV and state files;
- `requirements.txt` — Python dependencies.

## Collection behaviour

- First successful run: request publications from the previous 90 days.
- Later runs: request publications since the last successful run, with a 48-hour safety overlap.
- Duplicate URLs are removed.
- Stored records older than 365 days are removed.
- No paid AI service or API key is used.

The 90-day backfill is limited to records returned by the publisher's own API. It does not promise recovery of content that the source no longer exposes.

## Test it on GitHub

1. Copy the complete contents of this folder into the root of your GitHub repository.
2. Commit and push the files.
3. Open the repository on GitHub and select **Actions**.
4. Select **Daily ranking news collector**.
5. Click **Run workflow** and confirm the run.
6. Wait for the run to turn green.
7. Return to the repository. A bot commit named `Update ranking news data` should appear, together with:
   - `data/news.csv`;
   - `data/collector_status.csv`;
   - `data/run_state.json`.

That manual run tests exactly the same job and notebook used by cron. The scheduled trigger runs every day at 05:17 UTC.

If the collection succeeds but the final push receives a permissions error, open:

`Settings → Actions → General → Workflow permissions`

and allow **Read and write permissions**.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute ESMT_Rankings_Intelligence_Cron_Test.ipynb --output /tmp/cron_test.ipynb
streamlit run app.py
```

## Deploy the Streamlit page

After the first successful Action run, create a Streamlit Community Cloud app from the same repository and choose `app.py` as the main file. No separate backend or API is required for this test.

