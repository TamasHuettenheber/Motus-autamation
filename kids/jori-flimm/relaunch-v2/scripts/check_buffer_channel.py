#!/usr/bin/env python3
"""Read-only verification of Jori & Flimm's connected Buffer TikTok channel.

Required env: JORI_BUFFER_API_KEY (GitHub Actions secret), JORI_EXPECTED_TIKTOK_HANDLE.
Does not change queues, create posts, or touch MOTUS.
"""
import json, os, re, sys, urllib.error, urllib.request

API = "https://api.buffer.com"
def gql(query,variables=None):
    token=os.environ.get("JORI_BUFFER_API_KEY","")
    if not token:
        raise RuntimeError("JORI_BUFFER_API_KEY_NOT_SET - no external request")
    data=json.dumps({"query":query,"variables":variables or {}}).encode()
    req=urllib.request.Request(API,method="POST",data=data,headers={
        "Authorization":"Bearer "+token,
        "Content-Type":"application/json",
        "User-Agent":"JoriFlimm-ConnectionReadOnly/1.0"
    })
    try:
        with urllib.request.urlopen(req,timeout=30) as r:
            answer=json.load(r)
    except urllib.error.HTTPError as exc:
        raise RuntimeError("Buffer GraphQL HTTP "+str(exc.code)) from exc
    if answer.get("errors"):
        raise RuntimeError("Buffer GraphQL responded with errors; channel not verified")
    if not isinstance(answer.get("data"),dict):
        raise RuntimeError("Buffer GraphQL data not provided")
    return answer["data"]

def canonical_handle(v):
    return re.sub(r"^@","",str(v or "").strip().casefold())

def validate_channels(channels,expected):
    if not expected or expected == "motus614":
        raise ValueError("Expected isolated Jori & Flimm handle missing")
    valid=[x for x in channels if (str(x.get("service","")).lower()=="tiktok"
          and canonical_handle(x.get("name"))==expected)]
    if len(valid)!=1:
        raise RuntimeError("TARGET_TIKTOK_NOT_VERIFIED in Buffer (no posts created)")
    match=valid[0]
    if match.get("isQueuePaused"):
        raise RuntimeError("TARGET_BUFFER_QUEUE_PAUSED (nothing scheduled)")
    if not match.get("id"):
        raise RuntimeError("TARGET_TIKTOK_CHANNEL_ID_MISSING")
    return True

def main():
    expected=canonical_handle(os.environ.get("JORI_EXPECTED_TIKTOK_HANDLE","jori.flimm"))
    account=gql("query { account { organizations { id name } } }")
    orgs=(account.get("account") or {}).get("organizations") or []
    if not orgs:
        raise RuntimeError("BUFFER_HAS_NO_ORGANIZATIONS")
    collected=[]
    for org in orgs:
        oid=org.get("id")
        if not oid: continue
        query="query($id: OrganizationId!) { channels(input: {organizationId:$id}) { id name displayName service isQueuePaused } }"
        res=gql(query,{"id":oid})
        collected.extend(res.get("channels") or [])
    validate_channels(collected,expected)
    print("JORI_BUFFER_TIKTOK_CHANNEL_VERIFIED_READ_ONLY; expected @"+expected+
          "; no MOTUS actions, no drafts, no published posts.")

if __name__=="__main__":
    try:main()
    except Exception as exc:
        print("JORI_BUFFER_CONNECTION_NOT_VERIFIED: "+str(exc),file=sys.stderr)
        sys.exit(1)
