#!/bin/bash
set -euo pipefail

export SOURCE_DATE_EPOCH=$(git log -1 --format=%ct 2>/dev/null || echo 0)

JOBS="${2:-$(nproc)}"
MODE="${1:-release}"

case "${MODE}" in
    debug)
        echo "==> 配置 Release（含调试符号）..."
        cmake -B build \
            -DCMAKE_BUILD_TYPE="Release" \
            -DCMAKE_CXX_FLAGS_RELEASE="-O2 -DNDEBUG -g" \
            .
        echo ""
        echo "==> 编译 (${JOBS} 并行)..."
        cmake --build build --parallel "${JOBS}"

        EXE="build/pcl-cgre"
        [ -f "${EXE}.exe" ] && EXE="${EXE}.exe"

        echo ""
        echo "==> 分离调试符号..."
        objcopy --only-keep-debug "${EXE}" "${EXE}.debug"
        strip --strip-debug "${EXE}"

        echo "==> 完成: ${EXE} (stripped) + ${EXE}.debug (symbols)"
        ;;
    *)
        echo "==> 配置 Release..."
        cmake -B build -DCMAKE_BUILD_TYPE="Release" .
        echo ""
        echo "==> 编译 (${JOBS} 并行)..."
        cmake --build build --parallel "${JOBS}"
        echo "==> 完成: build/pcl-cgre"
        ;;
esac