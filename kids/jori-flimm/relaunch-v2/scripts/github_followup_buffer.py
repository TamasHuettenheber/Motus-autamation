#!/usr/bin/env python3
"""Schedule only validated Jori episodes 002–006; never touch MOTUS."""
import argparse,json,os,time,urllib.request,urllib.error
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
p=argparse.ArgumentParser();p.add_argument("--episode",type=int,required=True,choices=[2,3,4,5,6]);p.add_argument("--replace-existing",action="store_true");a=p.parse_args()
n=a.episode
key=os.environ.get("BUFFER_API_KEY","").strip()
assert key,"BUFFER_API_KEY_MISSING"
due=datetime(2026,10,22+n-1,14,0,tzinfo=ZoneInfo("Europe/Berlin"))
assert datetime.now(ZoneInfo("Europe/Berlin"))<due,"Requested publishing time passed"
expected_due_utc=due.astimezone(timezone.utc)
if n==6:
    release=json.loads(open("kids/jori-flimm/relaunch-v2/episode_006_release_record.json",encoding="utf-8").read())
    assert release.get("user_approved_for_publication") is True,"Episode 006 has no explicit user release approval"
    assert release.get("speech_caption_offset_accepted") is True,"Episode 006's accepted ending offset is not recorded"
    assert datetime.fromisoformat(release.get("target_due_at","")).astimezone(timezone.utc)==expected_due_utc,"Episode 006 release target differs from the fixed 14:00 slot"
repo=os.environ["GITHUB_REPOSITORY"]
version_suffix="-v2" if n==6 else ""
media=f"https://raw.githubusercontent.com/{repo}/feature/jori-flimm-neustart-folge001/published/jori-flimm-2026-10-{22+n-1:02d}-e{n:03d}{version_suffix}.mp4"
def gql(query,variables=None):
 req=urllib.request.Request("https://api.buffer.com",method="POST",data=json.dumps({"query":query,"variables":variables or {}}).encode(),headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"})
 try:
  with urllib.request.urlopen(req,timeout=45) as resp:result=json.load(resp)
 except urllib.error.HTTPError as exc:raise RuntimeError(f"Buffer HTTP {exc.code}: {exc.read()[:400]!r}")
 if result.get("errors"):raise RuntimeError(str(result["errors"]))
 return result["data"]
for attempt in range(16):
 try:
  with urllib.request.urlopen(urllib.request.Request(media,method="HEAD"),timeout=20) as resp:
   if resp.status==200 and int(resp.headers.get("Content-Length","0"))>1000000:break
 except Exception:pass
 time.sleep(5)
else:raise RuntimeError("Public GitHub MP4 not reachable; refusing Buffer")
orgs=gql("query{account{organizations{id name}}}")["account"]["organizations"]
matches=[]
for org in orgs:
 channels=gql("query($id:OrganizationId!){channels(input:{organizationId:$id}){id name displayName service}}",{"id":org["id"]})["channels"]
 for c in channels:
  names={str(c.get(k,"")).strip().lower().lstrip("@") for k in ["name","displayName"]}
  if str(c.get("service","")).lower()=="tiktok" and "jori.flimm" in names:matches.append((org["id"],c["id"]))
assert len(matches)==1,"Jori channel not uniquely verified; MOTUS must not be used"
oid,channel=matches[0]
query="query{posts(input:{organizationId:"+json.dumps(oid)+",filter:{status:[scheduled],channelIds:["+json.dumps(channel)+"]}}){edges{node{id text dueAt channelId}}pageInfo{hasNextPage}}}"
posts=gql(query)["posts"]
assert not posts["pageInfo"]["hasNextPage"],"Cannot check all scheduled posts"
existing=[]
for edge in posts["edges"]:
 old=edge["node"]
 if f"Jori & Flimm | Folge {n:03d}" in (old.get("text") or ""):
  existing.append(old)
if a.replace_existing:
 assert len(existing)==1,"Scheduled episode post is not unique; refusing replacement"
 old=existing[0]
 mutation="""mutation($input:EditPostInput!){editPost(input:$input){__typename ... on PostActionSuccess{post{id status dueAt channelId assets{mimeType source}}} ... on MutationError{message}}}"""
 edited=gql(mutation,{"input":{"id":old["id"],"assets":[{"video":{"url":media,"metadata":{"thumbnailOffset":1000}}}]}})["editPost"]
 assert edited.get("__typename")=="PostActionSuccess",edited
 post=edited["post"]
 assert post.get("id")==old["id"] and post.get("status")=="scheduled" and post.get("channelId")==channel,post
 assert post.get("dueAt")==old.get("dueAt"),{"before":old.get("dueAt"),"after":post.get("dueAt")}
 assert any(x.get("source")==media for x in post.get("assets",[])),post
 print("JORI_BUFFER_POST_UPDATED_IN_PLACE",n,json.dumps(post,ensure_ascii=False))
 raise SystemExit(0)
if existing:
 assert len(existing)==1,"Duplicate scheduled episode posts detected"
 old=existing[0]
 assert datetime.fromisoformat(old["dueAt"].replace("Z","+00:00")).astimezone(timezone.utc)==expected_due_utc,{"actual_dueAt":old.get("dueAt"),"expected_dueAt":due.isoformat()}
 print("JORI_EPISODE_ALREADY_SCHEDULED",n,old["id"],old["dueAt"])
 raise SystemExit(0)
if n==6:
 e=json.loads(open("kids/jori-flimm/relaunch-v2/episode_006_story_draft.json",encoding="utf-8").read())
else:
 data=json.loads(open("kids/jori-flimm/relaunch-v2/staffel1_folgen_001_005.json",encoding="utf-8").read())
 e=next(x for x in data["episodes"] if x["episode_number"]==n)
caption=f"Jori & Flimm | Folge {n:03d}: {e['title']}. Die Geschichte geht weiter – mit einem neuen Rätsel! #JoriUndFlimm #Kindergeschichte #Rätsel #GeschichtenFürKinder"
mutation="""mutation($input:CreatePostInput!){createPost(input:$input){__typename ... on PostActionSuccess{post{id status dueAt channelId assets{mimeType source}}} ... on MutationError{message}}}"""
result=gql(mutation,{"input":{"text":caption,"channelId":channel,"schedulingType":"automatic","mode":"customScheduled","dueAt":due.isoformat(timespec="milliseconds"),"aiAssisted":True,"metadata":{"tiktok":{"isAiGenerated":True}},"assets":[{"video":{"url":media,"metadata":{"thumbnailOffset":1000}}}]}})["createPost"]
assert result.get("__typename")=="PostActionSuccess",result
post=result["post"]
assert post.get("status")=="scheduled" and post.get("channelId")==channel,post
assert datetime.fromisoformat(post["dueAt"].replace("Z","+00:00")).astimezone(timezone.utc)==expected_due_utc,{"actual_dueAt":post.get("dueAt"),"expected_dueAt":due.isoformat()}
print("JORI_BUFFER_SCHEDULED_CONFIRMED",n,json.dumps(post,ensure_ascii=False))
