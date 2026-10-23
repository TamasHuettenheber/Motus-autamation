#!/usr/bin/env python3
"""Read-only verification of Jori & Flimm's connected Buffer TikTok channel.

Required env: BUFFER_API_KEY (existing MOTUS GitHub Actions secret), JORI_EXPECTED_TIKTOK_HANDLE.
The same API key may read multiple channels, but only the exact Jori & Flimm handle is accepted.
Does not change queues, create posts, or touch MOTUS.
"""
import json, os, re, sys, urllib.error, urllib.request

API = "https://api.buffer.com"
def gql(query,variables=None):
    token=os.environ.get("BUFFER_API_KEY","")
    if not token:
        raise RuntimeError("BUFFER_API_KEY_NOT_SET - existing MOTUS secret unavailable")
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
          and expected in {canonical_handle(x.get("name")),canonical_handle(x.get("displayName"))})]
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
    owning_org_by_channel={}
    for org in orgs:
        oid=org.get("id")
        if not oid: continue
        query="query($id: OrganizationId!) { channels(input: {organizationId:$id}) { id name displayName service } }"
        res=gql(query,{"id":oid})
        for channel in (res.get("channels") or []):
            collected.append(channel)
            if channel.get('id'):
                owning_org_by_channel[str(channel['id'])]=str(oid)
    validate_channels(collected,expected)
    target=next(x for x in collected if str(x.get("service","")).casefold()=="tiktok"
                and expected in {canonical_handle(x.get("name")),canonical_handle(x.get("displayName"))})
    org_id=owning_org_by_channel.get(str(target["id"]))
    if not org_id:
        raise RuntimeError("Buffer organization for target channel missing")
    # Separate account check; never read MOTUS's queue or create Buffer posts.
    query=("query { posts(input:{organizationId:"+json.dumps(org_id)+
           ",filter:{status:[scheduled],channelIds:["+json.dumps(str(target["id"]))+
           "]}}) { edges { node { id channelId dueAt text } } pageInfo { hasNextPage } } }")
    posts=(gql(query).get("posts") or {})
    rows=[edge.get("node",{}) for edge in posts.get("edges",[])]
    if posts.get("pageInfo",{}).get("hasNextPage"):
        raise RuntimeError("More queued posts than one page; manual queue verification needed")
    print("JORI_BUFFER_TIKTOK_CHANNEL_VERIFIED_READ_ONLY; expected @"+expected)
    print("JORI_BUFFER_QUEUED_POSTS="+str(len(rows))+"; no MOTUS actions")
    for post in rows:
        print("JORI_QUEUED="+str(post.get("dueAt",""))+" id="+str(post.get("id",""))+" text="+json.dumps(post.get("text",""),ensure_ascii=False))
    # Read all statuses from this Jori channel only, including today's first post.
    query=("query { posts(input:{organizationId:"+json.dumps(org_id)+
           ",filter:{channelIds:["+json.dumps(str(target["id"]))+
           "]}}) { edges { node { id channelId status dueAt sentAt externalLink text } } "
           "pageInfo { hasNextPage } } }")
    all_posts=(gql(query).get("posts") or {})
    channel_posts=[edge.get("node",{}) for edge in all_posts.get("edges",[])]
    first=[post for post in channel_posts
           if post.get("id")=="6ad9ce4baefa17e341f96c3f"
           or "Folge 001: Das Licht, das Joris Namen kannte" in (post.get("text") or "")]
    if len(first)==1:
        post=first[0]
        print("JORI_EPISODE001_BUFFER_STATUS="+str(post.get("status","unknown"))
              +" id="+str(post.get("id",""))
              +" dueAt="+str(post.get("dueAt",""))
              +" sentAt="+str(post.get("sentAt",""))
              +" externalLink="+str(post.get("externalLink","")))
    elif len(first)>1:
        print("JORI_EPISODE001_DUPLICATE_BUFFER_RECORDS="+str(len(first)))
    else:
        print("JORI_EPISODE001_NOT_FOUND_IN_BUFFER_CHANNEL"
              +" hasNextPage="+str(all_posts.get("pageInfo",{}).get("hasNextPage")))
    print("VERIFICATION_ONLY: no posts were created, scheduled or published")

if __name__=="__main__":
    try:main()
    except Exception as exc:
        print("JORI_BUFFER_CONNECTION_NOT_VERIFIED: "+str(exc),file=sys.stderr)
        sys.exit(1)
