#!/bin/bash

curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"fingerprint": "eJwty7kNADAMw8BVNILl-Mv-iwWCU11D0g_CQA-USIwoXNEg5YBH3o3-0sil7AHIrAyw", "lat": "-47.9", "lon": "-123.43"}' http://adhawk.sunlightfoundation.com/api/ad/
