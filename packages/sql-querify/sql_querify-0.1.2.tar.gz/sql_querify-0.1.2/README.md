# Querify
![Build Status](https://github.com/badihio/querify/actions/workflows/deploy.yml/badge.svg)

Querify is a CLI tool that provides SQL interface for data sources.
It is useful for data manipulation using a standard interface for various data sources, and provides an SQL features that allows to query the data in a more convenient way, like `WHERE`, `GROUP BY`, `ORDER BY` and `LIMIT`.

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install sql-querify
```
## Usage

```bash
qy <query>
```

## Examples
#### List all tables
```bash
qy "SHOW tables"
```
| table_name |
| ------ |
| dirs | 
| files |
| processes |

#### Describe a table
```bash
qy "DESC processes"
```
| field_name | data_type |
| ------ | ------ |
| pid| int |
| name| str|
| cmdline| str|
| status| str|
| username | str |
| cpu_pct | float|
| memory_pct | float |
| create_time| datetime |

#### Count processes by username
```bash
qy "SELECT username, COUNT(1) AS count FROM processes GROUP BY username ORDER BY count DESC"
```
| username | count |
| ------ | ------ |
| user1 |443 |
| root|215 |

#### Top 5 directories by size
```bash
qy "SELECT name, size_in_bytes/1024/1024 AS size_mb FROM dirs ORDER BY size_mb DESC LIMIT 5"
```
| name | size_mb |
| ------ | ------ |
| pydantic_core|4 |
| chardet|1 |
| distlib|1 |
| _vendor/rich/__pycache__ |1 |
| pip/_vendor/chardet|1 |

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
