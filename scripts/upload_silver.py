from __future__ import annotations

import argparse
import os
from pathlib import Path
from dotenv import load_dotenv

import boto3

load_dotenv()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    args = parser.parse_args()

    bucket = os.environ["ECOMMERCE_BUCKET"]
    region = os.getenv("AWS_REGION", "ap-northeast-2")
    src = Path("sample_data/silver") / f"dt={args.date}"

    if not src.exists():
        raise SystemExit(f"not found: {src}")

    s3 = boto3.client("s3", region_name=region)

    for path in sorted(src.iterdir()):
        if path.is_file():
            key = f"silver/dt={args.date}/{path.name}"
            print(f"{path} -> s3://{bucket}/{key}")
            s3.upload_file(str(path), bucket, key)

    print("[OK] Silver upload complete")


if __name__ == "__main__":
    main()
