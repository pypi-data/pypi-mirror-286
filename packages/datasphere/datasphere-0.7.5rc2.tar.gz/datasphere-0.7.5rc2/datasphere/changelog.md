# 0.7.4 (2024-06-24)

- Added command `download-files` for downloading completed job output files.

# 0.7.0 (2024-05-27)

- New features:
  -  Support for directories as input and output files.
  - `args` – arguments for job command line (`cmd`).
  - `fork` command, which allows to use another job as a template, overriding input/output files, 
     command line arguments, environment variables, docker image, working storage or cloud instance type.
  - Support of multiple cloud instance types (main and backoff-s).
  - Added GPU stats logger in `gpu_stats.tsv`.
- Minor bugfixes and improvements. 

# 0.6.12 (2024-04-03)

- Added commands to get and list projects – `project get`, `project list`.
- Added options for command output – `-o` to specify output file path (stdout by default) and `--format` to specify
  data format (tabular or json).

# 0.6.11 (2024-03-25)

- Support use case when main script is not in current working directory.
