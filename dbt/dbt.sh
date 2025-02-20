#!/bin/sh

set -ex

dbt --version
dbt run --target $PROFILE
