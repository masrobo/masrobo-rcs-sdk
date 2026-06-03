#!/usr/bin/env bash
# Java 单元测试运行脚本
# 用法：bash java/scripts/mvn-test.sh
cd "$(dirname "$0")/.." || exit 1
mvn test -Dsurefire.useFile=false