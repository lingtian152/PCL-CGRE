#!/bin/bash
set -euo pipefail


JOBS="${2:-$(nproc)}"

# 构建 release 文件
echo "==> 配置 release 配置..."
cmake -B build -DCMAKE_BUILD_TYPE="Release" .

echo ""
echo "==> 编译 (${JOBS} 并行)..."
cmake --build build --parallel "${JOBS}"

echo ""
echo "==> 完成: build/pcl-cgre_release"

# 构建 debug 文件
echo "==> 配置 debug 配置..."
cmake -B build -DCMAKE_BUILD_TYPE="Debug" .

echo ""
echo "==> 编译 (${JOBS} 并行)..."

cmake --build build --parallel "${JOBS}"

echo ""
echo "==> 完成: build/pcl-cgre_debug"