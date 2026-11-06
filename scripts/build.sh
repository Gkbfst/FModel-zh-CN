#!/usr/bin/env bash
# 编译单文件简中版 FModel.exe（Windows / .NET 10 SDK）
set -e
cd "$(dirname "$0")/.."

for f in "FModel/FModel.csproj" \
         "CUE4Parse/CUE4Parse/CUE4Parse.csproj" \
         "CUE4Parse/CUE4Parse-Conversion/CUE4Parse-Conversion.csproj" \
         "Snooper/Editor/Editor.csproj"; do
  if [ ! -f "$f" ]; then
    echo "缺少 $f"
    echo "请先执行: git submodule update --init --recursive"
    exit 1
  fi
done

echo "=== dotnet publish (Release / win-x64 / single-file) ==="
dotnet publish FModel/FModel.csproj \
  -c Release -r win-x64 --self-contained false \
  -o out \
  -p:PublishSingleFile=true \
  -p:IncludeNativeLibrariesForSelfExtract=true \
  -p:DebugType=None -p:DebugSymbols=false \
  --nologo -v:minimal

echo "=== 产物 ==="
find out -maxdepth 1 -type f -printf "%s %f\n" 2>/dev/null | sort -rn | head -10
