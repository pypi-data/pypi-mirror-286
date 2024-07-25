![TALP LOGO](https://pm.bsc.es/gitlab/dlb/talp-pages/-/raw/add-v1/talp_dlb_logo.png){height=250px}

# Talp Pages

TALP Pages is a collection of Python scripts to postprocess the `json` outputs of [DLB TALP](https://pm.bsc.es/ftp/dlb/doc/user-guide/intro.html#talp-tracking-application-live-performance) and Gitlab pipeline snippets [that can be included](https://docs.gitlab.com/ee/ci/yaml/#include) in your project.
This makes it easy to integrate TALP into your CI/CD setup and run Continous Benchmarking without having to code up your own solution.

**We provide:**

- talp_pages: Command line tool to generate static html pages
- Artifact management: A easy way to use Gitlab Artifacts to generate time series data plots.
- Reusable Jobs that easily integrate into a existing Gitlab CI enviroment

## Use python package

Talp-Pages is written in Python (3.9+). We rely on [poetry](https://python-poetry.org/) for packaging.
To use, simply install via:

```pip install talp-pages```

From there you should have the following command-line tools available:

- `talp_report`
- `talp_add_to_db`
- `talp_badge`
- `talp_report_ts`
- `talp_pages`
- `talp_download_artifacts`

## Use Gitlab Jobs

In order to use the GitlabJobs to generate the Talp Pages automagically, just adopt the configuration showcased in the [example application](https://gitlab.com/valentin.seitz1/sample-application)

We also provide documentation on the individual jobs:

- [add-to-db](gitlab-templates/add-to-db/README.md)
- [generate-html](gitlab-templates/generate-html/README.md)

## License

Talp-Pages is available under the General Public License v3.0.
