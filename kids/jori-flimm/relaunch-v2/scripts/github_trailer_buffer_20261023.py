#!/usr/bin/env python3
"""Publish only the one-off Jori trailer to Buffer with shareNow; no MOTUS changes."""
import json,os,sys,time,urllib.request,urllib.error
MARKER="Jori & Flimm | Willkommen bei Jori und Flimm | Trailer 2026-10-23"
CHANNEL="jori.flimm"
MEDIA=("https://raw.githubusercontent.com/TamasHuettenheber/Motus-autamation/"
       "feature/jori-flimm-neustart-folge001/published/jori-flimm-trailer-2026-10-23.mp4")
TOKEN=os.environ.get("BUFFER_API_KEY","").strip()
assert TOKEN,"Missing BUFFER_API_KEY; cannot publish"
def gql(query,variables=None):
  req=urllib.request.Request("https://api.buffer.com",method="POST",
       data=json.dumps({"query":query,"variables":variables or {}},ensure_ascii=False).encode(),
       headers={"Authorization":"Bearer "+TOKEN,"Content-Type":"application/json",
                "User-Agent":"JoriFlimmTrailer/1.0"})
  try:
    with urllib.request.urlopen(req,timeout=45) as response:data=json.load(response)
  except urllib.error.HTTPError as e:
    raise RuntimeError("Buffer HTTP "+str(e.code)+": "+e.read(400).decode(errors="replace")) from e
  if data.get("errors"):raise RuntimeError("Buffer GraphQL: "+str(data["errors"]))
  return data["data"]
def rows_for_org(orgid,channelid):
  query=("query {posts(input:{organizationId:"+json.dumps(orgid)
         +",filter:{channelIds:["+json.dumps(channelid)+"]}})"
         "{edges{node{id text status sentAt dueAt externalLink channelId}}pageInfo{hasNextPage}}}")
  res=gql(query)["posts"]
  if res["pageInfo"]["hasNextPage"]:raise RuntimeError("Posts paginated; cannot prove uniqueness")
  return [e["node"] for e in res["edges"]]
def main():
  orgs=gql("query{account{organizations{id name}}}")["account"]["organizations"]
  matches=[]
  for org in orgs:
    cs=gql("query($id:OrganizationId!){channels(input:{organizationId:$id}){id name displayName service}}",
       {"id":org["id"]})["channels"]
    for c in cs:
      handles={str(c.get("name","")).lower().lstrip("@"),str(c.get("displayName","")).lower().lstrip("@")}
      if str(c.get("service","")).lower()=="tiktok" and CHANNEL in handles:
        matches.append((org["id"],c["id"]))
  assert len(matches)==1,"Jori channel not uniquely verified; NO publication"
  oid,cid=matches[0]
  rows=rows_for_org(oid,cid)
  existing=[p for p in rows if MARKER in (p.get("text") or "")]
  if existing:
    assert len(existing)==1,"Duplicate trailers found"
    p=existing[0]
    print("JORI_TRAILER_ALREADY_EXISTS_NO_DUPLICATE",json.dumps(p,ensure_ascii=False))
    return
  for k in range(18):
    try:
      with urllib.request.urlopen(urllib.request.Request(MEDIA,method="HEAD"),timeout=20) as response:
        size=int(response.headers.get("Content-Length","0"))
        if response.status==200 and size>1_000_000:break
    except Exception:pass
    time.sleep(5)
  else:raise RuntimeError("GitHub trailer MP4 not publicly available; Buffer NOT called")
  caption=(MARKER+
     "\nPsst! Ein Stern, ein Rätsel und zwei neue Freunde. "
     "Lerne Jori und Flimm kennen und folge @jori.flimm, "
     "damit du keine Folge unseres magischen Abenteuers verpasst! "
     "#JoriUndFlimm #Kindergeschichte #Rätselabenteuer #Kinderbuch #Geschichten")
  mutation="""mutation($input:CreatePostInput!){createPost(input:$input){__typename
   ... on PostActionSuccess{post{id text channelId status sentAt dueAt externalLink shareMode assets{mimeType source}}}
   ... on MutationError{message}}}"""
  created=gql(mutation,{"input":{"text":caption,"channelId":cid,"schedulingType":"automatic",
     "mode":"shareNow","aiAssisted":True,"metadata":{"tiktok":{"isAiGenerated":True}},
     "assets":[{"video":{"url":MEDIA,"metadata":{"thumbnailOffset":1000}}}]}})["createPost"]
  assert created.get("__typename")=="PostActionSuccess",created
  p=created["post"]
  assert p.get("channelId")==cid, "Buffer returned different channel"
  print("JORI_TRAILER_BUFFER_SHARE_NOW_ACCEPTED",json.dumps(p,ensure_ascii=False))
  # Buffer publishing is asynchronous. Verify actual sent status rather than assuming.
  for i in range(6):
    entries=rows_for_org(oid,cid)
    found=[x for x in entries if x.get("id")==p["id"]]
    if len(found)==1:
      latest=found[0]
      print("JORI_TRAILER_BUFFER_STATUS",json.dumps(latest,ensure_ascii=False))
      if latest.get("status")=="sent":
        print("JORI_TRAILER_PUBLISHED_CONFIRMED",latest.get("externalLink") or "external link pending")
        return
      if latest.get("status")=="error":raise RuntimeError("Buffer post errored: "+str(latest))
    time.sleep(10)
  print("JORI_TRAILER_BUFFER_ACCEPTED_BUT_NOT_YET_SENT: do NOT claim TikTok published")
if __name__=="__main__":main()
