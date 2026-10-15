---
title: "From Laptop to Lakehouse: Analytical SQL with DuckDB"
talkId: "17558"
conference: devoxx-be-2026
speakers: [Oliver Geisser]
track: "Cloud Native, Data & Infrastructure"
sessionType: Tools-in-Action
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=B5-4mDLrWjM
durationMin: 29
slides: null
verdict: 7
frames: 6
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# From Laptop to Lakehouse: Analytical SQL with DuckDB

Oliver Geisser · Tools-in-Action · Cloud Native, Data & Infrastructure

## TL;DR

DuckDB is an open-source, in-process analytical SQL engine with no server and no dependencies, and this demo-driven session walks it from a laptop CLI through embedded Java and Python apps to S3 queries and a DuckLake lakehouse. The arc ends with Quack, the remote client/server protocol that adds multi-user access to DuckLake, demoed here on a 2.0 alpha. Every step runs live on screen, and the demo repository is published for replay.

## Key takeaways

- DuckDB embeds as a C++ library in any process: the CLI, a JDBC driver in plain Java, or the Python library all run queries with no network hop.
- CSV, Parquet, JSON, Excel and SQLite files are queryable directly with auto-detected schema and delimiters, and the `SELECT *` and `read_csv` wrappers can be omitted when the filename suffix implies the extension.
- The same SQL reads remote files over HTTPS and S3 through a filesystem abstraction layer; credentials stay in persistent secrets in the user home, separate from source code.
- `ATTACH` connects several databases at once (in-memory, file, SQLite, Postgres), so one query joins across a data lake, a relational database and a local file.
- DuckLake pairs Parquet data files on object storage with a plain SQL catalog database (DuckDB for local use, Postgres or MySQL for production), which keeps multi-file ACID semantics without a bespoke catalog service.
- DuckDB's read/write file lock blocks a second client, so multi-user DuckLake needs either a server-backed catalog or Quack, the remote protocol that turns one DuckDB process into a server others connect to.

## Notes

### [00:34](https://youtu.be/B5-4mDLrWjM?t=34) What DuckDB is

Geisser opens on duckdb.org: open-source, in-process (embedded in the host process), and analytical, meaning a column-oriented storage model that is fast at queries and aggregations but not at single-row transactions. He states up front this is a demo-driven talk with no slides; the demos live in directories backed by a GitHub repository with markdown guides. Starting the CLI bare gives an in-memory database, while passing a filename persists to disk; the shell is multi-line (statements end with a semicolon), has syntax highlighting, history, and dot commands such as `.databases` and `.tables`.

### [04:20](https://youtu.be/B5-4mDLrWjM?t=260) Embedding in Java and Python

The Java example is deliberately boring: plain JDBC with only the DuckDB JDBC driver as a dependency, runnable via JBang, working the same under Spring or plain code. One performance note: because JDBC iterates result sets row-wise while DuckDB stores column-wise, the team added a `DuckDBConnection` class that operates on chunks. The Python version is structurally identical (import library, connect, execute, print), and both print the same result. Behind both sits the same in-process C++ library.

### [07:36](https://youtu.be/B5-4mDLrWjM?t=456) Reading local files

A directory of CSV, JSON, Parquet, Excel and SQLite samples shows how little ceremony each format needs. `read_csv` auto-detection infers the delimiter and column types (a double and a date are detected on screen); overrides exist when detection fails. A Parquet import loads 14.86 million rows into the in-memory database with an interactive progress bar, and DuckDB spills to disk rather than crashing on larger-than-memory files. Syntax shortcuts follow: the extension can be inferred from the filename suffix, so a bare `FROM 'file.csv'` or `FROM 'taxi_trips.parquet'` just works once extensions are loaded.

### [11:13](https://youtu.be/B5-4mDLrWjM?t=673) Remote files and S3

The filesystem abstraction treats local and remote paths identically: public HTTPS data is queried with no extra tool, and S3 (or Azure) reads use the same syntax against a prepared bucket. No credentials appear on screen because they live in persistent secrets, one for S3 and one for Postgres, stored in the user home directory and kept out of source control.

### [13:21](https://youtu.be/B5-4mDLrWjM?t=801) Attaching multiple databases

`.databases` shows two live connections at once: the in-memory database holding the imported taxi_trips and beach_clubs tables, and a persistent DuckDB file with a bikes table. Attaching SQLite and then Postgres extends the same engine further, and DuckDB translates its simplified syntax into each backend's dialect. The payoff is cross-engine joins: a data lake, a Postgres database and an emailed local file analysed in one query. Postgres, MySQL and ODBC-accessible engines such as SQL Server are all supported through extensions.

### [16:29](https://youtu.be/B5-4mDLrWjM?t=989) DuckLake: a lakehouse from files plus SQL

Current lakehouse stacks layer Parquet files, JSON metadata and a catalog service, and Geisser relays the DuckDB team's argument that the catalog can be an ordinary SQL database under almost no load, since the heavy data stays in Parquet on object storage. DuckLake is therefore two things: a standard-SQL catalog specification plus object storage. Three live setups demonstrate the range: a local DuckDB catalog with local files (a `main/shakespeare` directory holding a single `ducklake-*.parquet` file, with more files appearing on writes), a local catalog with S3 storage, and Postgres as catalog with S3 storage. All three attach to one engine simultaneously.

### [22:22](https://youtu.be/B5-4mDLrWjM?t=1342) Quack: multi-user access via client/server

The production gap is DuckDB's exclusive write lock on its database file: a second read/write client blocks, which is why production DuckLake currently needs Postgres or MySQL (read-only frozen lakes excepted). The answer is Quack, the remote protocol due end of October 2026, demoed here on a 2.0 alpha. One process attaches the S3-backed lake and becomes a server listening on a port; a second shell starts its own alpha client, attaches to the server over Quack, and `USE`s the lake, after which both show the same Shakespeare tables. Query execution happens server-side against S3, giving a cost-efficient alternative to cloud-provider lakehouses that scales with object storage while many small clients share one low-load catalog.

### [27:43](https://youtu.be/B5-4mDLrWjM?t=1663) Resources

The closing slide lists the talk repository (github.com/ogeisser/duckdb-talk), duckdb.org, ducklake.select, and shell.duckdb.org, where DuckDB compiled to WebAssembly runs fully in the browser with no installation.

## Tools, libraries and specs

- DuckDB (CLI, JDBC driver, Python library; 2.0 alpha for the Quack demo)
- DuckLake (catalog spec; ducklake.select)
- Quack (DuckDB remote client/server protocol, demoed on the 2.0 alpha)
- JBang (runs the Java JDBC demo)
- Postgres, MySQL, SQLite, SQL Server via ODBC (attachable backends)
- AWS S3 (object storage for remote reads and DuckLake data files)
- shell.duckdb.org (in-browser DuckDB via WebAssembly)

## Who should watch

Developers and data engineers who want serverless SQL analytics over files, object storage or mixed sources without standing up infrastructure. Skip it if you already run DuckDB with remote storage and DuckLake in production; the three-topology DuckLake setup and the Quack alpha walkthrough are the parts that go beyond the docs.

## Verdict

**7/10**: the whole arc from CLI to a Quack client/server loop runs on screen and the demo repository covers every segment, but the material is documented DuckDB usage and no performance, cost or scale claim carries a number.

**Novelty 1/2**

- **+** [20:50](https://youtu.be/B5-4mDLrWjM?t=1250) The speaker's own demo set attaches three DuckLake setups (local catalog with local files, local catalog with S3, Postgres catalog with S3) to one engine at once.
- **−** A search for the subject returns the DuckDB docs (ATTACH, CSV import, httpfs) and the ducklake.select spec covering this material; the talk runs no comparison and reports no original result.

**Demonstrated 2/2**

- **+** [06:34](https://youtu.be/B5-4mDLrWjM?t=394) The JBang Java demo runs, then the Python demo prints the same result.
- **+** [26:07](https://youtu.be/B5-4mDLrWjM?t=1567) The Quack client attaches to the server, runs `connect`, and shows the S3-backed `shakespeare` table (87643 rows) beside the server's `lake_s3`, completing the client/server loop on screen.
- **−** [14:25](https://youtu.be/B5-4mDLrWjM?t=865) The cross-engine join across a lake, Postgres and a local file is pitched as "in my sample data this does not make sense", and no join result appears.

**Measured 0/2**

- **−** [01:37](https://youtu.be/B5-4mDLrWjM?t=97) "Really fast in querying and aggregations" comes with no query timing or comparison, and "it will not crash" on larger-than-memory files ([09:40](https://youtu.be/B5-4mDLrWjM?t=580)) is stated without a spill run.
- **−** [09:30](https://youtu.be/B5-4mDLrWjM?t=570) The import shows a progress bar ("~1 second remaining" at 77%) and "Memory: 2.5 GB" for 14.86 million rows, but no elapsed time or baseline, and the speaker ties them to no claim.
- **−** [26:41](https://youtu.be/B5-4mDLrWjM?t=1601) "Very cost-efficient", "into the terabytes" and "not a bottleneck" come with no cost, scale or latency figures.

**Depth 2/2**

- **+** [01:37](https://youtu.be/B5-4mDLrWjM?t=97) In-process plus column-oriented storage is given as the reason DuckDB is fast at queries and aggregations and weaker at single-row transactions.
- **+** [17:02](https://youtu.be/B5-4mDLrWjM?t=1022) The DuckLake rationale is explained: the catalog database carries almost no load because the heavy data stays in Parquet on object storage.
- **+** [21:51](https://youtu.be/B5-4mDLrWjM?t=1311) The exclusive write lock on a read/write database file is the stated reason a second client blocks, which is why production DuckLake needs Postgres today and Quack once released.

**Reusable 2/2**

- **+** [27:43](https://youtu.be/B5-4mDLrWjM?t=1663) The closing slide points to github.com/ogeisser/duckdb-talk, which has one guide per talk segment, runnable Java and Python demos, sample data and a Postgres setup script.
- **−** [02:10](https://youtu.be/B5-4mDLrWjM?t=130) Replay needs Git LFS for the large sample files (~710 MiB), and the S3 and Postgres demos rely on the speaker's own bucket and secrets.
